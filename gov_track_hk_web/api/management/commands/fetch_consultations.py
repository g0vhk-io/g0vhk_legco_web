# -*- coding: utf-8 -*-
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from api.models import Consultation
from datetime import *
from dateutil.parser import *
import os
import json
import requests
import lxml.html
from io import StringIO
import functools
from urlparse import urlsplit
from urlparse import urljoin
import md5
from django.db.utils import IntegrityError
class Command(BaseCommand):
    help = 'Fetch Consultations'

    def handle(self, *args, **options):
        for lang in ['en', 'tc', 'sc']:
            url = 'http://www.gov.hk/%s/residents/government/publication/consultation/current.htm' % (lang)
            r = requests.get(url) 
	    print r.apparent_encoding
            root = lxml.html.fromstring(r.text)
	    print r.text.encode("utf-8")
            table = root.xpath("//div[@class='innerPageHolder articleHolder']/section/table/tbody")[0]
            rows = table.xpath("tr")
            for row in rows[1:]:
                title_cell, date_cell = row.xpath("td")
                title = title_cell.xpath("a/text()")[0]
                link = title_cell.xpath("a/@href")[0]
                link = urljoin(url, link)
                date_str = date_cell.xpath("text()")[0]
                date = datetime.strptime(date_str,"%d.%m.%Y")
                d = {"title": title, "lang": lang, "date": date, "link": link}
                c = Consultation()
                c.lang = lang
                c.title = title.encode("utf-8")
		print title.encode("utf-8")
		print c.title
                c.link = link
                c.key = str(md5.new(link).hexdigest())
                c.date = date 
                try:
                    c.save()
                except IntegrityError:
                    print "Already inserted"
