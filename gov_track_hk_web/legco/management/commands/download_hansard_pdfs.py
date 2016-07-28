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

class Command(BaseCommand):
    help = 'Download the hansards PDFs'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)


    @transaction.atomic
    def handle(self, *args, **options):
        for yr in [12, 13, 14, 15]:
            r = requests.get('http://www.legco.gov.hk/webcast_data/yr%d-%d/counmtg_agenda.js' % (yr, yr + 1))
            for line in [l[1:-2] for l in r.text.split()[1:-2] if l.find('=') != -1]:
                pairs = line.split(',')
                for a,b in [p.split('=') for p in pairs]:
                    d = "%s-%s-%s" % (a[0:4], a[4:6], a[6:])
                    rundown_request = requests.get('http://www.legco.gov.hk/php/hansard/chinese/rundown.php?date=%s&lang=2' % (d))
                    rundown_html = rundown_request.text.split('\n')
                    for line in rundown_html:
                        if line.find(".pdf") != -1:
                            var, url = line.split(" = ")
                            url = url.strip()
                            pdf_url = url.replace("\"", "").replace(";", "").replace("#", "").replace("\\", "")
                            file_name = pdf_url.split('/')[-1]
                            print "%s,%s" % (pdf_url, file_name)
                            pdf_request = requests.get(pdf_url)
                            f = open('pdfs/' + file_name , 'wb')
                            f.write(pdf_request.content)
                            f.close()

