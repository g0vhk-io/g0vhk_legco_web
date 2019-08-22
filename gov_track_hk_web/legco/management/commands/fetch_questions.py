# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
from lxml.html.clean import clean_html
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from legco.models import Bill,  BillCommittee, BillThirdReading, BillFirstReading, BillSecondReading, Individual, Question
from lxml import etree
from datetime import *
from dateutil.parser import *
from hashlib import md5
from lxml.html.clean import Cleaner
from django.db.utils import *
import re



url_pattern = "http://www.legco.gov.hk/yr%d-%d/chinese/counmtg/question/ques%d%d.htm"
year_ranges = [(15, 16)]

def all_text(node):
    return "".join([x for x in node.itertext()])

class Command(BaseCommand):
    help ='Fetch Questions'

    def handle(self, *args, **options):
        individuals = Individual.objects.all()
        for y1, y2 in year_ranges:
            url = url_pattern % (y1, y2, y1, y2)
            r = requests.get(url)
            r.encoding = "utf-8"
            output = r.text
            root = etree.HTML(output)
            dates = [d.text for d in root.xpath("//h2[@class=\"h3_style\"]/a[contains(@href,\"agenda\")]")]
            tables = root.xpath("//table[@class=\"interlaced\"]")
            if len(dates) != len(tables):
                raise Exception("Dates and Questions Mismatch! %d <> %d" % (len(dates), len(tables)) )

            for i in range(0, len(dates)):
                date = datetime.strptime(dates[i], '%d.%m.%Y')
                print(date)
                table = tables[i]
                for row in table.xpath(".//tr")[1:]:
                    cells = row.xpath("td")
                    if all_text(cells[3]).strip() == '-':
                        continue
                    legislator_name = cells[1].text
                    if legislator_name.startswith(u"郭偉强"):
                        legislator_name = u"郭偉強"
                    title = all_text(cells[2])
                    question_type_text = all_text(cells[0])
                    individual = None
                    for p in individuals:
                        if legislator_name.startswith(p.name_ch):
                            individual = p
                            break
                    if individual is None:
                        print(legislator_name)
                        raise Exception("Individual not found. " , legislator_name)
                    link = cells[3].xpath(".//a")[0].attrib['href']
                    key = str(md5.new(link).hexdigest())
                    m = re.match(r"(.*[0-9]+|UQ)[\(]{0,1}(.*)\)", question_type_text)
                    if m is None:
                        raise Exception("Undefined Question Type", link, question_type_text)
                    question_type = m.group(2)
                    detail_r = requests.get(link)
                    detail_r.encoding = "big5"
                    output = detail_r.text
                    cleaner = Cleaner(comments=False)
                    output = cleaner.clean_html(output)
                    detail_root = etree.HTML(output)
                    try:
                        press_release = all_text(detail_root.xpath("//div[@id=\"pressrelease\"]")[0])
                    except IndexError:
                        detail_r = requests.get(link)
                        detail_r.encoding = "utf-8"
                        output = detail_r.text
                        output = cleaner.clean_html(output)
                        detail_root = etree.HTML(output)
                        press_release = all_text(detail_root.xpath("//span[@id=\"pressrelease\"]")[0])
                    question_start = press_release.find(u'以下')
                    reply_start = press_release.rfind(u'答覆：')
                    question_text = press_release[question_start:reply_start]
                    answer_text = press_release[reply_start + 3:]
                    #print(question_text)
                    #print(answer_text)
                    #print(link)
                    #print(date)
                    #print(individual.name_en)
                    #print(key)
                    #print(question_type)
                    question = Question()
                    question.key = key
                    question.individual = individual
                    question.date = date
                    question.question_type = question_type
                    question.question = question_text
                    question.answer = answer_text
                    question.title = title
                    question.link = link
                    question.title_ch = title
                    try:
                        question.save()
                    except IntegrityError:
                        print("%s %s already exists" % (str(date),title))
