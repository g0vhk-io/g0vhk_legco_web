# -*- coding: utf-8 -*
from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, date
register = template.Library()

@register.filter
def parse_date_chinese(d):
    if d is datetime and d.replace(tzinfo=None) == datetime.min:
        return "未知"
    return "%d年%d月%d日" % (d.year, d.month, d.day)

@register.filter
def is_date_min(d):
	return  d.replace(tzinfo=None) == datetime.min
