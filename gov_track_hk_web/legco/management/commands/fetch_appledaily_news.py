# -*- coding: utf-8 -*-
import sys, traceback
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary, NewsArticle, Party
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

def fetch(item, d):
    try:
        r = requests.get(item['link'])
        r.encoding = "utf-8"
        root = etree.HTML(r.text)

        print item['link']
        item['title'] = root.xpath("//table[@class=\"LinkTable\"]/tr/td/h1")[0].text.strip()
        item['image'] = root.xpath("//meta[@property=\"og:image\"]")[0].attrib['content'].strip()
        item['text'] = ''.join([s.strip() for s in root.xpath("//div[@id=\"masterContent\"]")[0].itertext()]).strip()
        print item['text']
        print item['title']
        print item['image']
    except Exception as e:
        raise
        print "cannot parse %s" % (item['link'])
        print e
    return item

class Command(BaseCommand):
    help = 'Fetch Apple Daily News'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str)


    def handle(self, *args, **options):
        d = options["date"]
        r = requests.get('http://hk.apple.nextmedia.com/archive/index/%s/index/' % d)
        r.encoding = "utf-8"
        root = etree.HTML(r.text)       
        links = []
        for a in root.xpath("//a"):
            href = a.attrib.get('href', '')
            m = re.match(r'(http|https)://hk.apple.nextmedia.com(/[^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*)', href)
            if m is None:
                m = re.match(r'(http|https)://hk.apple.nextmedia.com(/[^/]*)/([^/]*)/([^/]*)/([^/]*)', href)
            if m is not None:
                g = list(m.groups())
                if g[-2] == d and g[-1] != "index" and g[-3] != "index":
                    links.append(href) 
        #items = [fetch({'link': link}, d) for link in links] 
        items = [{'link': link} for link in list(set(links))]
        #    items.append({'author': author, 'title': title, 'link': link, 'description': description, 'image': image})
        print("Number of Items %d on %s" % (len(items), d))
        fetch({'link': 'http://hk.apple.nextmedia.com/financeestate/art/20160901/19756230'}, d)
        pool = multiprocessing.Pool(16)
        result = pool.map_async(functools.partial(fetch, d=d), items)
        items = result.get()
        individuals = Individual.objects.all()
        parties = Party.objects.all()
        for item in items:
            article = NewsArticle()
            article.link = item['link']
            article.title = item['title']
            article.text = item['text']
            article.image = item['image']
            article.date = datetime.strptime(d, '%Y%m%d').date()
            article.source = 'applehk'
            article.key =  str(md5.new(article.link).hexdigest())
            try:
                article.save()
                article.individuals = []
                for individual in individuals:
                    if article.text.find(individual.name_ch) != -1:
                        print("article %s relates to %s" % (individual.name_ch, article.title))
                        article.individuals.add(individual)
                article.parties = []
                for party in parties:
                    if article.text.find(party.name_ch) != -1:
                        print("article %s relates to %s" % (party.name_ch, article.title))
                        article.parties.add(party)
                article.save()
            except IntegrityError as e:
                print("Failed to add %s due to integriy" % (article.title))
                traceback.print_exc()
                pass
