# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.cache import cache
import requests
import dateutil.parser
from django.contrib.syndication.views import Feed
from gov_track_hk_web.settings import MORPH_IO_API_KEY
from subscriber.models import News
from django.utils import feedgenerator
import md5
import datetime
# Create your views here.

class ConsultationsFeed(Feed):
    title = u"g0vhk.io 現正刊登的諮詢文件"
    link = "/consultations.xml"
    feed_type = feedgenerator.Rss201rev2Feed
    def items(self):
        key = "consultations_json"
        cached_items = cache.get(key)
        if cached_items is None:
            url = "https://api.morph.io/howawong/hong_kong_current_consultation_pages/data.json?key=%s&query=select%%20*%%20from%%20'data'%%20limit%%20100" % (MORPH_IO_API_KEY)
            r = requests.get(url)
            items = [r for r in  r.json() if r['lang'] == 'tc']
            items = sorted(items, key=lambda item: item['date'], reverse=True)
            cache.set(key, items, 24 * 60 * 60)
            cached_items = items
        return cached_items

    def item_title(self, item):
        return item['title']

    def item_description(self, item):
        return item['title']

    def item_link(self, item):
        return item['link']

    def item_pubdate(self, item):
        return dateutil.parser.parse(item['date'])

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
        return str(md5.new(item.date.strftime('%Y-%m-%d') + item.title_ch.encode("utf-8")).hexdigest())

    def item_pubdate(self, item):
        return datetime.datetime.combine(item.date, datetime.time(0,0,0))
