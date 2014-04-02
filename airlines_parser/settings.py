# Scrapy settings for aa100 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)   # '/airlines_parser'
from tinypanel import settings as main_settings
BOT_NAME = 'airlines_parser'
SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'
# Setting up django's project full path.

sys.path.insert(0, main_settings.BASE_DIR)   # '/airlines_parser'

# Setting up django's settings module name.
# This module is located at /home/rolando/projects/myweb/myweb/settings.py.

os.environ['DJANGO_SETTINGS_MODULE'] = 'tinypanel.settings'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'aa100 (+http://www.yourdomain.com)'

# all setting for parser:

