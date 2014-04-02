# -*- coding: utf-8 -*-
import re
from django.utils.html import strip_tags

__author__ = 'vladimir'

def html_to_clean_text(html):
    return strip_tags(re.sub(' +',' ',html).replace('\n', ''))


def safe_list_get(list, index, default=None):
    """
    Safe way to access a[10], if exception?return default value
    """
    try:
        return list[index]
    except IndexError:
        return default