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
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
import re
import sys

sys.setrecursionlimit(2000)

def delete_extra_space(s):
    return re.sub('([^\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', '\\1\\2', s)

def parse_layout(layout, output):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
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
    toc = list()
    for (level,title,dest,a,structelem) in document.get_outlines():
        action = a.resolve()
        dest = resolve1(document.get_dest(action['D']))
        t = (pages[dest['D'][0].objid], dest['D'][3], title)
        toc.append(t)
        #print resolve1(obj['Contents']).get_data()

    page_texts = []
    page_no = 0
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        output = []
        parse_layout(layout, output)
        output = sorted(output, key=lambda x: x[0][3], reverse=True)
        page_texts += [(page_no, bbox[1], bbox[3], text ) for bbox, text in output if bbox[1] <= 750]
        page_no += 1
    return toc, page_texts


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)
        parser.add_argument('--url', type=str)


    @transaction.atomic
    def handle(self, *args, **options):
        individuals = Individual.objects.all()
        file_path = options['file']
        url = options['url']
        m = re.match('cm(\d\d\d\d)(\d\d)(\d\d).*\.pdf', file_path.split('/')[-1])
        date = None
        if m is not None:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            date = datetime(year, month, day)
        print date
        tocs, page_texts = get_toc(file_path)
        toc_index = -1
        total_tocs = len(tocs)
        total_texts = len(page_texts)
        t_index = 0
        texts_by_toc = [[]]
        whole_msg = ""
        seq_no = 0
        bookmark = ""
        result = []
        while t_index < total_texts:
            text = page_texts[t_index]
            if toc_index + 1 < total_tocs:
                next_toc = tocs[toc_index + 1]
                if text[0] == next_toc[0] and (next_toc[1] >= text[1]):
                    result.append((seq_no, bookmark, delete_extra_space(whole_msg).strip()))
                    toc_index += 1
                    seq_no += 1
                    bookmark = next_toc[2].strip()
                    whole_msg = ""
                    texts_by_toc.append([])
            msg = text[3]
            msg = msg.strip()
            msg = re.sub('([^\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', '\\1\\2', msg)
            if len(msg) == 0:
                whole_msg += "\n"
            else:
                whole_msg += msg
            texts_by_toc[-1].append(text)
            t_index += 1
        result.append((seq_no, bookmark, delete_extra_space(whole_msg).strip()))
        hansard = MeetingHansard()
        hansard.key = str(md5.new(url).hexdigest())
        hansard.source_url = url
        hansard.date = datetime.min
        hansard.save()
        for r in result:
            speech = MeetingSpeech()
            speech.individual = None
            if r[1].startswith("SP"):
                speech.title_ch = r[2][0:r[2].find(u'：')]
                speech.title_ch = speech.title_ch.replace(u"郭偉强" ,u"郭偉強")
                dot_pos = speech.title_ch.find('.')
                if dot_pos != -1:
                    speech.title_ch = speech.title_ch[dot_pos + 1:]
                for individual in individuals:
                    if speech.title_ch.startswith(individual.name_ch):
                        speech.individual = individual
            if r[1] == "":
                s = r[2].replace(" ", "")
                date_match = re.search(u"(\d+)年(\d+)月(\d+)日", s)
                date = datetime(int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3)))
                print date
            if r[1] == "mbp" or r[1] == "mba" or r[1] == "poa" or r[1] == "cia":
                lines = [l for l in r[2].split("\n") if len(l) > 0][1:]
                for line in lines:
                    title = re.sub(r'[a-zA-Z\-]', '', line.split(",")[0]).strip()
                    title = title.replace(u"郭偉强" ,u"郭偉強")
                    personel = MeetingPersonel()
                    personel.title_ch = title
                    for i in individuals:
                        if title.find(i.name_ch + u"議員") != -1:
                            personel.individual = i
                            break
                    personel.save()
                    if r[1] == "mbp":
                        hansard.members_present.add(personel)
                    if r[1] == "mba":
                        hansard.members_absent.add(personel)
                    if r[1] == "poa":
                        hansard.public_officers.add(personel)
                    if r[1] == "cia":
                        hansard.clerks.add(personel)
                    print "[%s][%s]" % (personel.individual is not None,personel.title_ch)
            speech.text_ch = r[2]
            speech.bookmark = r[1]
            speech.sequence_number = r[0]
            #print
            #print "%d %s %s %s" % (r[0], r[1], speech.title_ch, speech.individual)
            speech.save()
            hansard.speeches.add(speech)
        if date is None:
            raise Exception("Date cannot be determined.")
        hansard.date = date
        hansard.save()
        print "New Hansard ID=%d" % hansard.id
