from django.contrib import admin

from .models import Article, Report

admin.site.register(Article)
admin.site.register(Report)