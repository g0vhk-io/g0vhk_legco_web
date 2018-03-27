from django.contrib import admin

from subscriber.models import News, Subscriber

# Register your models here.

admin.site.register(Subscriber)
admin.site.register(News)
