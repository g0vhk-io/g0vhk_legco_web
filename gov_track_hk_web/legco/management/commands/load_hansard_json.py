# -*- coding: utf-8 -*-
from django.db import transaction
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from legco.models import Meeting, Vote, Motion, Individual, IndividualVote, VoteSummary, Party, MeetingHansard, MeetingSpeech, MeetingPersonel
from dateutil.parser import *
import os
import json
import requests
import multiprocessing
from lxml import etree
from io import StringIO
import functools
import hashlib
import re
import sys
import json
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Load hansard JSON into database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def delete_existing_hansard(self, url):
        try:
            hansard = MeetingHansard.objects.get(source_url=url)
            queries = [hansard.members_present,
                       hansard.speeches,
                       hansard.members_absent,
                       hansard.public_officers,
                       hansard.clerks]
            for q in queries:
                for o in q.all():
                    o.delete()
                q.clear()
            hansard.delete()
        except ObjectDoesNotExist:
            pass

    def process_members(self, members, all_individuals):
        all_personels = []
        for line in members:
            title = re.sub(r'[a-zA-Z\-]', '', line.split(",")[0]).strip()
            title = title.replace(u"郭偉强" ,u"郭偉強")
            if title.startswith(u"#"):
                continue
            personel = MeetingPersonel()
            personel.title_ch = title
            for i in all_individuals:
                if title.find(i.name_ch + u"議員") != -1:
                    personel.individual = i
                    break
            personel.save()
            all_personels.append(personel)
        return all_personels

    def process_speeches(self, speeches, all_individuals):
        output = []
        for data in speeches:
            speech = MeetingSpeech()
            bookmark = data["bookmark"]
            content = data["content"]
            speech.individual = None
            if bookmark.startswith("SP"):
                speech.title_ch = data["title"]
                speech.title_ch = speech.title_ch.replace(u"郭偉强" ,u"郭偉強")
                dot_pos = speech.title_ch.find('.')
                if dot_pos != -1:
                    speech.title_ch = speech.title_ch[dot_pos + 1:]
                for individual in all_individuals:
                    if speech.title_ch.startswith(individual.name_ch):
                        speech.individual = individual
            speech.text_ch = content
            speech.bookmark = bookmark
            speech.sequence_number = data["sequence"]
            speech.save()
            output.append(speech)
        return output

    @transaction.atomic
    def handle(self, *args, **options):
        all_individuals = Individual.objects.all()
        file_path = options['file']
        with open(file_path) as f:
            s = f.read()
            payload = json.loads(s)
            hansard_date = datetime.strptime(payload["date"], '%Y-%m-%d')
            hansard_url = payload["url"]
            self.delete_existing_hansard(hansard_url)
            hansard = MeetingHansard()
            md5 = hashlib.md5()
            md5.update(hansard_url.encode('utf-8'))
            hansard.key = str(md5.hexdigest())
            hansard.source_url = hansard_url
            hansard.date = hansard_date
            hansard.save()
            members_present = self.process_members(payload["membersPresent"], all_individuals)
            members_absent = self.process_members(payload["membersAbsent"], all_individuals)
            public_officers = self.process_members(payload["publicOfficersAttending"], all_individuals)
            clerks = self.process_members(payload["clerksInAttendance"], all_individuals)
            speeches = self.process_speeches(payload["speeches"], all_individuals)
            for m in members_present:
                hansard.members_present.add(m)
            for m in members_absent:
                hansard.members_absent.add(m)
            for p in public_officers:
                hansard.public_officers.add(p)
            for c in clerks:
                hansard.clerks.add(c)
            for s in speeches:
                hansard.speeches.add(s)
            print("New hansard ID=%d" % hansard.id)
            hansard.save()
