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
        articles = NewsArticle.objects.filter(source = 'mingpao')
        for article in articles:
            if article.date is None:
                d_s = urlsplit(article.link).path.split('/')[-3]
                d = datetime.strptime(d_s, '%Y%m%d').date()
                article.date = d
                article.save()
            
