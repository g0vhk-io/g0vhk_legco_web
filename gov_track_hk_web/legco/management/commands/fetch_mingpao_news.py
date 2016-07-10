# -*- coding: utf-8 -*-
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary, NewsArticle, Party
from datetime import *
from dateutil.parser import *
import os
import json
import requests
import execjs
import multiprocessing
from lxml import etree
from io import StringIO
import functools

def fetch(item, d, e):
    url = item['link']
    path_last = url.split("/")[-1]
    js_url = "http://news.mingpao.com/dat/pns/pns_web_tc/article1/%s%s/todaycontent_%s.js" % (d, e, path_last)
    r = requests.get(js_url)
    r.encoding = "utf-8"
    try:
        j = r.json()
        item['text'] = j['DESCRIPTION']
        return item
    except Exception as e:
        print("Something wrong at " + js_url + " " + url)
        print(j.text)
        raise e


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str)

    def handle(self, *args, **options):
        j = json.loads(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'issuelist.json'), 'rb').read().decode("utf-8"))
        d = options["date"]
        e = j['PNS_WEB_TC']['1 ' + d]['E'].lower()
        url = "http://news.mingpao.com/dat/pns/pns_web_tc/feed1/%s%s/content.js" % (d, e)
        print("Fetching from:" +url)
        js = requests.get(url).text
        line = "function foo(){ \n" + js.split('\n')[2][0:-2].replace("feed2['content_%s%s']=" % (d, e), 'return ') +"}"
        ctx = execjs.compile(line)
        output = ctx.call("foo")
        items = []
        for k in output.keys():
            for item in output[k]['rss']['channel']['item']:
                if item['LINK'].find('s00018') != -1 or item['LINK'].find('s00021') != -1:
                    continue

                media_group = item.get('media:group', None)
                image = None
                if media_group is not None:
                    media_content = next((x for x in media_group if 'media:content' in x), None)
                    if media_content is not None:
                        image_element = media_content['media:content'][-1]
                        image = "http://fs.mingpao.com/" + image_element['ATTRIBUTES']["URL"]
                author = item['AUTHOR']
                title = item['TITLE']
                link = "http://news.mingpao.com" + item['LINK']
                description = item['DESCRIPTION']
                if title not in [u'要聞',u'港聞',u'社評‧筆陣',u'論壇',u'中國',u'國際',u'經濟',u'體育',u'影視',u'副刊',u'英文']:
                    #print("%s,%s,%s,%s" % (author, title, link, description))
                    items.append({'author': author, 'title': title, 'link': link, 'description': description, 'image': image})
        print("Number of Items %d on %s" % (len(items), d))
        fetch(items[0], d, e)
        pool = multiprocessing.Pool(8)
        result = pool.map_async(functools.partial(fetch, d=d, e=e), items)
        items = result.get()
        individuals = Individual.objects.all()
        parties = Party.objects.all()
        for item in items:
            article = NewsArticle()
            article.link = item['link']
            article.title = item['title']
            article.text = item['text']
            article.image = item['image']
            article.source = 'mingpao'
            try:
                article.save()
                print("Added %s" % (article.title))
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
                pass
