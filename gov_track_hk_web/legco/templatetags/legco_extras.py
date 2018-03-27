# -*- coding: utf-8 -*
from django import template
import random
from datetime import datetime
register = template.Library()


@register.filter
def parse_date_chinese(d):
    if d is datetime and d.replace(tzinfo=None) == datetime.min:
        return "未知"
    return "%d年%d月%d日" % (d.year, d.month, d.day)


@register.filter
def article_source_chinese(s):
    if s == "mingpao":
        return "明報"
    if s == "applehk":
        return "蘋果日報"
    return ""


@register.filter
def is_date_min(d):
    return d.replace(tzinfo=None) == datetime.min


@register.simple_tag
def random_label():
    labels = ["label-default",
              "label-primary",
              "label-success",
              "label-info",
              "label-warning",
              "label-danger"]
    return labels[random.randint(0, len(labels) - 1)]


@register.simple_tag
def random_panel(i=-1):
    labels = ["default",
              "primary",
              "success",
              "info",
              "warning",
              "danger"]
    if i == -1:
        i = random.randint(0, len(labels) - 1)
    return "panel-" + labels[i]


@register.filter
def vote_result_chinese(result):
    return "通過" if result.lower() == "passed" else "否決"


@register.filter
def vote_result_color(result):
    return "#00ff00" if result.lower() == "passed" else "#ff0000"


@register.filter
def vote_chinese(v):
    d = {'YES': '贊成',
         'NO': '反對',
         'ABSTAIN': '棄權',
         'PRESENT': '出席',
         'ABSENT': '缺席'}
    return d[v]
