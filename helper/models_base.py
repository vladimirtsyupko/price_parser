# -*- coding: utf-8 -*-
from django.db import models


class CoreItem(models.Model):
    class Meta:
        abstract = True


class TimeItem(CoreItem):
    when_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, blank=True, null=True)
    when_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True


class MetaItem(CoreItem):
    meta_title = models.TextField(verbose_name='Мета-тайтл', max_length=150, blank=True, default='', null=True)
    meta_description = models.TextField(verbose_name='Мета-описание', max_length=250, blank=True, default='', null=True)
    meta_keywords = models.TextField(verbose_name='Мета-ключи', max_length=250, blank=True, default='', null=True)

    class Meta:
        abstract = True

