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
BOT_NAME = 'prices_parser'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

COMMANDS_MODULE = 'commands'
SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'
DEFAULT_ITEM_CLASS = 'items.ParsedPriceItem'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36'
DOWNLOAD_DELAY = 0.8

ITEM_PIPELINES = {
    'pipelines.ImagesStorePipeline': 1000,
    'pipelines.CsvExportPipeline': 1000,
    #'prices.pipelines.SQLiteStorePipeline'
    'pipelines.MySQLStorePipeline': 1000,
}
# ITEM_PIPELINES = {}
WEBSERVICE_ENABLED = True
EXTENSIONS = {
    'scrapy.contrib.corestats.CoreStats': 500,
    'scrapy.webservice.WebService': 500,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}
CONCURRENT_REQUESTS_PER_DOMAIN = 10
CONCURRENT_REQUESTS = 10
RANDOMIZE_DOWNLOAD_DELAY = False
#LOG_FILE = 'prices.log'
LOG_LEVEL = 'DEBUG'
#COOKIES_DEBUG = True
URLLENGTH_LIMIT = 5000
AWS_ACCESS_KEY_ID = r"AKIAJIGHJQ3H2MDN7SLA"
AWS_SECRET_ACCESS_KEY = r"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"
#s3 = boto.connect_s3(aws_access_key_id = AWS_ACCESS_KEY_ID,aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

IMAGES_EXPIRES = 90
#IMAGES_STORE = r'f:/img/'
IMAGES_STORE = main_settings.MEDIA_ROOT
# IMAGES_STORE = 's3://www.tinypanel.com/img/'
IMAGES_THUMBS = {
    'normal': (350, 350),
    'icon': (165, 165),
}


# Setting up django's project full path.
import sys
sys.path.insert(0, main_settings.BASE_DIR)   # '/airlines_parser'

# Setting up django's settings module name.
# This module is located at /home/rolando/projects/myweb/myweb/settings.py.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tinypanel.settings'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'aa100 (+http://www.yourdomain.com)'

# all setting for parser:

