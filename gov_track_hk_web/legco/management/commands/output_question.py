import requests
from lxml.html.clean import clean_html
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from legco.models import Bill,  BillCommittee, BillThirdReading, BillFirstReading, BillSecondReading, Individual, Question
from lxml import etree
from datetime import *
from dateutil.parser import *
import md5
from lxml.html.clean import Cleaner
from django.db.utils import *
import re
import json

class Command(BaseCommand):
    help ='Fetch Questions'

    def handle(self, *args, **options):
        questions = Question.objects.prefetch_related('individual').all()
        l = [{'individual': q.individual.name_en, 'question': q.question, 'answer': q.answer, 'type': q.question_type, 'date': datetime.strftime(q.date, "%Y-%m-%d")} for q in questions]
        print(json.dumps(l))

