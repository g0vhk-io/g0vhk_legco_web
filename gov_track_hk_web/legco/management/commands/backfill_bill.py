# -*- coding: utf-8 -*-
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary, NewsArticle, Party, MeetingHansard, MeetingSpeech
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
from legco.models import *
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import scraperwiki
def delete_extra_space(s):
    return re.sub('([^\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', '\\1\\2', s)

class Command(BaseCommand):
    help = 'Backfill Bill Information'

    def add_arguments(self, parser):
        pass


    @transaction.atomic
    def handle(self, *args, **options):
        bills = Bill.objects.all()
        for bill in bills:
            print "Bill #%d" %(bill.id)
            saved = False
            pdf_url = bill.bill_content_url_ch
            r  = requests.get(pdf_url)
            print pdf_url
            pdf = scraperwiki.pdftoxml(r.content)
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            root = etree.fromstring(pdf.encode('utf-8'), parser=parser)
            pages = root.xpath('//page')
            for page in pages:
                texts = page.xpath("text")
                doc = ""
                texts = sorted(texts, key=lambda x: int(x.attrib['top']))
                for text in texts:
                    left = int(text.attrib['left'])
                    if left > 600:
                        continue
                    doc += "".join([x for x in text.itertext()])
                #print doc.encode("utf-8")
                m = re.match(r'(.*)旨在(.*)(由立法會制(定|訂)。|弁言)', doc.encode("utf-8"))
                if m is not None:
                    print "[" + m.group(2) + "]"
                    bill.description = m.group(2)
                    bill.save()
                    saved = True
                    break
            if not saved:
                raise Exception("bill pdf at " + pdf_url + ", description not found.")
                #print "##########"
