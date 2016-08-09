# -*- coding: utf-8 -*-
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary, NewsArticle, Party, MeetingHansard, MeetingSpeech, MeetingPersonel
from datetime import *
from dateutil.parser import *
import os
import json
import requests
import multiprocessing
from lxml import etree
from io import StringIO
import functools
import md5
from pdfminer.psparser import PSKeyword, PSLiteral
from pdfminer.pdftypes import PDFStream, PDFObjRef, resolve1, stream_value
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTChar, LTRect, LTCurve
import re
import sys

sys.setrecursionlimit(2000)

def delete_extra_space(s):
    return re.sub('([^\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', '\\1\\2', s)

def parse_layout(layout, output):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox):
            for a in lt_obj:
                output.append((a.bbox,a.get_text()))
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj, output)  # Recursive


def get_toc(pdf_path):
    infile = open(pdf_path, 'rb')
    parser = PDFParser(infile)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    pages = dict( (page.pageid, pageno) for (pageno, page)
                               in enumerate(PDFPage.create_pages(document)) )
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_texts = []
    page_no = 0
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        output = []
        parse_layout(layout, output)
        output = sorted(output, key=lambda x: (int(x[0][1] / 5) * 5, int(10000 -x[0][0])), reverse=True)
        page_texts += [(page_no, int(bbox[1] / 5) * 5, bbox[0], text ) for bbox, text in output if bbox[1] <= 770 and bbox[1] >= 45]
        page_no += 1
    return page_texts


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)


    @transaction.atomic
    def handle(self, *args, **options):
        individuals = Individual.objects.all()
        file_path = options['file']
        m = re.match('fc(\d\d\d\d)(\d\d)(\d\d).*\.pdf', file_path.split('/')[-1])
        date = None
        if m is not None:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            date = datetime(year, month, day)
        print date
        tocs, page_texts = get_toc(file_path)
        texts = []
        for page_no, y0, x0, text in page_texts:
            text = text.strip()

            if len(text) == 0:
                continue
            text = text.encode("utf-8")

            text = re.sub('([^\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', '\\1\\2', text)
            pos = text.find('：')
            if pos != -1:
                if pos > 0:
                    texts.append(text[0:pos].strip())
                texts.append(text[pos + 3 :].strip())
            else:
                texts.append(text)
        total_lines = len(texts)
        c = 0
        texts_by_titles = {}
        titles = ["出席委員", "缺席委員", "出席公職人員", "列席秘書", "法律顧問", "項目"]
        for title in titles:
            texts_by_titles[title] = []
        should_stop = False
        while c < total_lines and not should_stop:
            hit_title = False
            for title in titles:
                if texts[c].startswith(title):
                    if title == titles[-1]:
                        should_stop = True
                        break
                    hit_title = True
                    print "======%s====" % (title)
                    c = c + 1
                    while c < total_lines:
                        found = False
                        for t in titles:
                            if texts[c].startswith(t):
                                found = True
                                break
                        if found:
                            break
                        print "%s,%s"% (title, texts[c])
                        texts_by_titles[title].append(texts[c])
                        c = c + 1
                    break
            if not hit_title:
                c = c + 1
            if should_stop:
                break
        results = []
        while c < total_lines:
            if re.match("\d+\.", texts[c]) is not None:
                msg = ""
                c = c + 1
                while c < total_lines and re.match("\d+.", texts[c]) is None:
                    msg = msg + texts[c]
                    c = c + 1
                results.append(msg)
            else:
                c = c + 1

        hansard = MeetingHansard()
        hansard.key = str(md5.new(file_path.split('/')[-1]).hexdigest())
        hansard.source_url = file_path.split('/')[-1]
        hansard.date = datetime.min
        hansard.meeting_type = "fc"
        hansard.save()
        seq_no = 0
        for line in texts_by_titles["出席委員"]:
            t = None

            line = line.replace("郭偉强" ,"郭偉強")
            pos = line.find(", ")
            if pos != -1:
                line = line[0:pos ]
            for i in individuals:
                if i.name_ch.encode("utf-8") + "議員" == line:
                    t = i
                    break
            if t is None:
                raise Exception("Member not found.")
            member = MeetingPersonel()
            member.individual = t
            member.title_ch = line
            member.save()
            hansard.members_present.add(member)


        for line in texts_by_titles["缺席委員"]:
            t = None
            line = line.replace("郭偉强" ,"郭偉強")
            pos = line.find(", ")
            if pos != -1:
                line = line[0:pos]
            for i in individuals:
                if i.name_ch.encode("utf-8") + "議員" == line:
                    t = i
                    break
            if t is None:
                raise Exception("Member not found.", line)
            member = MeetingPersonel()
            member.individual = t
            member.title_ch = line
            member.save()
            hansard.members_absent.add(member)
        public_lines = texts_by_titles["出席公職人員"]
        total_public_lines = len(public_lines)
        z = 0
        while z < total_public_lines:
            msg = public_lines[z]
            z += 1
            while z < total_public_lines and public_lines[z].find("先生") == -1 and public_lines[z].find("女士") == -1:
                msg += public_lines[z]
                z += 1
            p = MeetingPersonel()
            p.individual = None
            p.title_ch = msg
            p.save()
            hansard.public_officers.add(p)


        for r in results:
            speech = MeetingSpeech()
            speech.sequemce_number = seq_no
            r = r.replace("郭偉强" ,"郭偉強")
            speech.text_ch = r
            speech.bookmark = ""
            speech.save()

            found_individuals = []
            for i in individuals:
                if r.find(i.name_ch.encode("utf-8") + "議員") != -1:
                    found_individuals.append(i)
            if len(found_individuals) > 0:
                speech.individual = found_individuals[0]
                speech.title_ch = speech.individual.name_ch
                for i in found_individuals[1:]:
                    speech.others_individual.add(i)
            speech.save()
            hansard.speeches.add(speech)
            seq_no += 1
        if date is None:
            raise Exception("Date cannot be determined.")
        hansard.date = date
        hansard.save()
        print "New Hansard ID=%d" % hansard.id
