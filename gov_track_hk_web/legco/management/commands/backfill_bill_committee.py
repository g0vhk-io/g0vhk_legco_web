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
import re
from legco.models import *
from urlparse import urljoin

def find_individual(title_ch, individuals):
    title_ch = title_ch.replace(u"李慧", u"李慧琼")
    title_ch = title_ch.replace(u"郭偉强", u"郭偉強")
    for individual in individuals:
        if title_ch.startswith(individual.name_ch + u"議員"):
            return individual
    msg = "Individual not found: [%s]" % (title_ch)
    print msg
    raise Exception(msg)

def node_text(node):
    return "\n".join([x.strip()  for x in node.itertext()])

class Command(BaseCommand):
    help = 'Backfill Bill Information'

    def add_arguments(self, parser):
        pass


    @transaction.atomic
    def handle(self, *args, **options):
        bills = Bill.objects.all()
        individuals = Individual.objects.all()
        for bill in bills:
            print "Bill #%d" %(bill.id)
            committee = bill.committee
            url = committee.bills_committee_url_ch
            if len(url) == 0:
                continue
            general_page_request = requests.get(url)
            general_page_request.encoding = 'utf-8'
            root = etree.HTML(general_page_request.content)
            links = root.xpath("//a/@href")
            committee_link = ""
            for link in links:
                if "_mem" in link:
                    committee_link = urljoin(url, link)
            saved = False
            if len(committee_link) > 0:
                print committee_link
                committee_request = requests.get(committee_link)
                parser = etree.HTMLParser(remove_comments=True)
                detail_root = etree.fromstring(committee_request.content, parser=parser)
                table = detail_root.xpath("//table")[0]
                rows = table.xpath(".//tr")
                chairman_name = ""
                member_names = []
                vice_chairman_name = ""
                for row in rows:
                    cells = row.xpath(".//td")
                    if len(cells) != 2:
                        continue
                    key = node_text(cells[0]).strip()
                    key = re.sub(r'\s+', '', key, flags=re.UNICODE)
                    value = node_text(cells[1]).strip()
                    if key == u"主席":
                        chairman_name = value
                    if key == u"副主席":
                        vice_chairman_name = value
                    if key == u"委員":
                        member_names = value.split("\n")
                chairman = find_individual(chairman_name, individuals)
                vice_chairman = None
                if len(vice_chairman_name) > 0:
                    vice_chairman = find_individual(vice_chairman_name, individuals)
                print chairman_name
                print vice_chairman_name
                print member_names
                committee.chairman = chairman
                committee.vicechairman = vice_chairman
                committee.individuals = []
                total_member_names = len(member_names)
                for i, n in enumerate(member_names):
                    try:
                        committee.individuals.add(find_individual(n, individuals))
                    except Exception:
                        if i != total_member_names - 1:
                            print n
                            raise Exception(n)
                committee.save()
                saved = True
            if not saved:
                print url
                print committee_link
                print committee.id
                #print "##########"
