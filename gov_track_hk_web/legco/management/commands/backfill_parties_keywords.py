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
from urlparse import urlsplit

class Command(BaseCommand):
    help = 'Backfill mingpao article date'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        articles = NewsArticle.objects.all()
        c = articles.count()
        x = 0
        parties = Party.objects.all()
        while x < c:
            for article in articles[x: x + 100]:
                for party in parties:
                    if party.keywords is not  None:
                        keywords = [s for s in [s.strip() for s in party.keywords.split(',')] if len(s) > 0]
                        for keyword in keywords:
                            if article.text.find(keyword) != -1:
                                print("article %s relates to %s" % (keyword.encode("utf-8"), article.title.encode("utf-8")))
                                article.parties.add(party)
                article.save()
            x += 100
