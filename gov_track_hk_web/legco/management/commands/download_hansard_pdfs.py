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

def get_cm_dates(year):
    url = "http://www.legco.gov.hk/general/chinese/counmtg/yr16-20/mtg_%d%d.htm" % (year, year + 1)
    r = requests.get(url)
    r.encoding = "utf-8"
    root = etree.HTML(r.text)
    links = [re.match(r'.*date=([^&]+)', link).group(1) for link in root.xpath("//a/@href") if link.find("date=") != -1]
    return list(set(links))


class Command(BaseCommand):
    help = 'Download the hansards PDFs'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        for yr in [16, 17]:
            for d in get_cm_dates(yr):
                rundown_request = requests.get('http://www.legco.gov.hk/php/hansard/chinese/rundown.php?date=%s&lang=2' % (d))
                rundown_html = rundown_request.text.split('\n')
                for line in rundown_html:
                    if line.find(".pdf") != -1:
                        var, url = line.split(" = ")
                        url = url.strip()
                        pdf_url = url.replace("\"", "").replace(";", "").replace("#", "").replace("\\", "")
                        file_name = pdf_url.split('/')[-1]
                        year , month, day = d.split("-")
                        dest = 'pdfs/' + 'cm%s%s%s-confirm-ec.pdf'% (year, month, day)
                        print "%s,%s" % (pdf_url, dest)
                        pdf_request = requests.get(pdf_url)
                        f = open(dest , 'wb')
                        f.write(pdf_request.content)
                        f.close()

