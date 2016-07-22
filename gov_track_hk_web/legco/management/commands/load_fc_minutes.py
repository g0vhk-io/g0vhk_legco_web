# -*- coding: utf-8 -*-
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary, NewsArticle, Party, MeetingHansard, MeetingSpeech, MeetingPersonel
from legco.models import FinanceMeetingItem, FinanceMeetingItemEvent, FinanceMeetingResult
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
import urlparse
from django.db.models import Q

sys.setrecursionlimit(2000)
url_format =  "http://www.legco.gov.hk/yr%d-%d/chinese/fc/fc/general/meetings.htm"
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        yr = 15
        url = url_format % (yr, yr + 1)
        r = requests.get(url)
        r.encoding = "utf-8"
        root = etree.HTML(r.text)
        links = root.xpath("//a/@href")
        for link in links:
            if "results/fc" in link and link.endswith(".htm"):
                link_abs = urlparse.urljoin(url, link)
                print link_abs
                file_name = link_abs.split('/')[-1]
                date_m = re.match('fc(\d\d\d\d)(\d\d)(\d\d).htm', file_name)
                date = datetime(year=int(date_m.group(1)), month=int(date_m.group(2)), day=int(date_m.group(3)))

                meeting = None
                try:
                    meeting = Meeting.objects.get(Q(date__year = date.year) & Q(date__month = date.month) & Q(date__day = date.day) & Q(meeting_type = "Finance Committee"))
                    print "Meeting found"
                except Meeting.DoesNotExist:
                    print "Meeting not found"
                    #raise Exception("Meeting not found.", date)
                detail_request = requests.get(link_abs)
                detail_request.encoding = "utf-8"
                detail_root = etree.HTML(detail_request.text)
                div = detail_root.xpath("//div[@id=\"_content_\"]")[0]
                tables = div.xpath("./table")
                table = None
                if len(tables) == 0:
                    table = div.xpath("div/table")[-1]
                else:
                    table = tables[-1]
                items = []
                for row in table.xpath("tr")[1:]:
                    cells = row.xpath("td")
                    vote = None
                    for a_node in cells[1].xpath(".//a"):
                        item_title = "".join([x for x in a_node.itertext()]).strip().encode("utf-8").strip()
                        item_pdf_link = urlparse.urljoin(link_abs, a_node.attrib['href'])
                        print item_title, item_pdf_link
                        break
                    description = "".join([x for x in cells[2].itertext()]).strip().encode("utf-8")
                    print "description=[%s]" % (description)
                    decision = "".join([x for x in cells[3].itertext()]).strip().encode("utf-8")
                    if "點名表決" in decision:
                        vote_link  = cells[3].xpath("a/@href")[0]
                        print "vote_link=[%s]" % vote_link
                        m = re.match(".*v(\d\d\d\d)(\d\d)(\d\d)(\d).pdf", vote_link)
                        if m is None:
                            m = re.match(".*fc\d+v(\d+)_tpc.pdf", vote_link)
                            vote_number = int(m.group(1))
                        else:
                            vote_number = int(m.group(4))
                        print "vote_number=[%d]" % (vote_number)
                        if meeting is not None:
                            vote = Vote.objects.filter(Q(meeting__pk = meeting.id) & Q(vote_number = vote_number)).first()
                    decision = re.sub(r"\(.*\)", r"", decision, flags=re.DOTALL).strip()
                    print "decision=[%s]" % decision
                    item, created = FinanceMeetingItem.objects.get_or_create(key=item_title)
                    if created:
                        item.key = item_title
                        item.description = description
                        item.source = item_pdf_link
                        item.save()
                    event = FinanceMeetingItemEvent()
                    event.decision = decision
                    event.date = date
                    event.vote = vote
                    event.item = item
                    event.save()

                result = FinanceMeetingResult()
                result.key = str(md5.new(link_abs).hexdigest())
                result.source = link_abs
                result.meeting = meeting
                result.save()
