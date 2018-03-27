# -*- coding: utf-8 -*-
from datetime import datetime, time, timedelta
from hashlib import md5

import dateutil.parser
import requests
from django.contrib.syndication.views import Feed
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.utils import feedgenerator

from api.models import Consultation
from subscriber.models import News

# Create your views here.

class ConsultationsFeed(Feed):
    title = u"g0vhk.io 現正刊登的諮詢文件"
    link = "/consultations.xml"
    feed_type = feedgenerator.Rss201rev2Feed
    def items(self):
        now = datetime.now()
        earlier = now - timedelta(days=30)
        consultations = Consultation.objects.filter(Q(lang = "tc") & Q(date__gte=earlier))
        items = [{'date': c.date, 'link': c.link, 'title': c.title, 'lang': c.lang} for c in consultations]
        items = sorted(items, key=lambda item: item['date'], reverse=True)
        return items

    def item_title(self, item):
        return item['title']

    def item_description(self, item):
        return item['title']

    def item_link(self, item):
        return item['link']

    def item_pubdate(self, item):
        return item['date']

class NewsFeed(Feed):
    title = u"g0vhk.io 最新消息"
    link = "/news.xml"
    feed_type = feedgenerator.Rss201rev2Feed
    def items(self):
        news = News.objects.all().order_by('-date')[0:10]  
        return news

    def item_title(self, item):
        return item.title_ch

    def item_description(self, item):
        return item.text_ch

    def item_link(self, item):
        return "http://g0vhk.io"

    def item_guid(self, item):
        m = md5()
        m.update(item.date.strftime('%Y-%m-%d') + item.title_ch.encode("utf-8"))
        return str(m.hexdigest())

    def item_pubdate(self, item):
        return datetime.combine(item.date, time(0,0,0))
