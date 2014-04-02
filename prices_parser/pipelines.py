import datetime
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem
from scrapy import log, signals
import MySQLdb
import traceback
from scrapy.contrib.pipeline.images import ImagesPipeline
import sqlite3
from os import path
import os
import time
import unicodedata
# import boto
from tinypanel.settings import MYSQL_USER_HOST, MYSQL_USER_LOGIN, MYSQL_USER_PASSWD, MYSQL_USER_DB,  \
    SQLITE_PATH
import gspread
import hashlib
from scrapy.http import Request


class ImagesStorePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            log.msg("get_media_requests: Saving " + item['image'], log.DEBUG)
            log.msg('image: ' + str(item['image']), log.DEBUG)
            if not 'unavailable' in item['image'].lower().replace('%20', ' '):
                yield Request(str(item['image']))
        except:
            pass

    def item_completed(self, results, item, info):
        log.msg('results ' + str(results), log.DEBUG)
        self.image_paths = ''.join([x['path'] for ok, x in results if ok])
        #if not self.image_paths:
        #    raise DropItem("Item contains no images")
        item['image'] = self.image_paths
        return item


class CsvExportPipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        file = open('%s_%s.csv' % (spider.name, int(time.time())), 'w+b')
        self.files[spider] = file
        #self.exporter = CsvItemExporter(file,fields_to_export = ['pid','price','curr','date','source','title','heading','url','sku','in_stock','image'],dialect='excel',delimiter=';')
        self.exporter = CsvItemExporter(file, fields_to_export=['product_id', 'price', 'price_usd', 'currency', 'when_created',
                                                                'source', 'title', 'heading', 'url', 'in_stock',
                                                                'image'], dialect='excel')
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if item is None:
            raise DropItem("None")
        self.exporter.export_item(item)
        return item


class MySQLStorePipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.conn = MySQLdb.connect(user=MYSQL_USER_LOGIN, passwd=MYSQL_USER_PASSWD, db=MYSQL_USER_DB,
                                    host=MYSQL_USER_HOST, charset="utf8", use_unicode=True)
        self.cur = self.conn.cursor()
        self.ADD_ITEM = """
        INSERT INTO price_parser_product_price
        (shop_id, product_id, price, price_usd, currency, source, heading, in_stock, url, image, when_created)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        # self.CHK_ITEM = "SELECT * FROM prices_images WHERE pid = %s;"
        self.CHK_ITEM1 = """
        SELECT * FROM price_parser_product_price WHERE product_id = %s and source = %s and DATE(when_created) = %s;
        """

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):

        # self.types = {'full': 0, 'thumbs/normal': 1, 'thumbs/icon': 2}
        today = datetime.date.today()
        if self.CheckItemDBThreeFields(item['product_id'], item['source'], today):
            try:
                self.cur.execute(self.ADD_ITEM,
                                 (item['shop_id'],
                                  item['product_id'],
                                  item['price'],
                                  item['price_usd'],
                                  item['currency'],
                                  item['source'],
                                  item['heading'],
                                  item['in_stock'],
                                  item['url'],
                                  item['image'],
                                  item['when_created'],
                                 ))
            except:
                log.msg("Unable to add Item " + str(item['product_id']), log.ERROR, spider=spider)
                log.msg(traceback.format_exc(), log.ERROR)
            self.conn.commit()
        else:
            log.msg(
                "Item with pid = '" + str(item['product_id']) + "' for date = '" + str(item['when_created']) + "' source = '" + str(
                    item['source']) + "' skipped as duplicate", log.DEBUG, spider=spider)

        # if self.CheckItemDBOneField(item['product_id']):
        #     # for k, v in self.types.iteritems():
        #     try:
        #         self.cur.execute("INSERT INTO prices_images (pid,type,path) VALUES (%s,%s,%s)",
        #                          (
        #                              item['pid'],
        #                              v,
        #                              k + item['image_paths'].replace('full', '')
        #                          ))
        #         self.conn.commit()
        #     except:
        #         log.msg("Unable to store img " + str(item['image_paths']), log.ERROR, spider=spider)
        #         log.msg(traceback.format_exc(), log.ERROR)
        #
        # for k in item.iterkeys():
        #     try:
        #         item[k] = unicodedata.normalize('NFKD', item[k]).encode('ascii', 'ignore')
        #     except:
        #         pass


        return item

    # def CheckItemDBOneField(self, ID):
    #     self.cur.execute(self.CHK_ITEM, (str(ID),))
    #     if self.cur.fetchone() is None:
    #         return True
    #     return False

    def CheckItemDBThreeFields(self, ID1, ID2, ID3):
        self.cur.execute(self.CHK_ITEM1, (str(ID1), str(ID2), str(ID3),))
        if self.cur.fetchone() is None:
            return True
        return False


class SQLiteStorePipeline(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.conn = sqlite3.connect(SQLITE_PATH)
        self.cur = self.conn.cursor()
        #type: 0-full;1-normal;2-icon
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS prices_prices (id INTEGER PRIMARY KEY AUTOINCREMENT, pid INTEGER, price NUMERIC, price_usd NUMERIC, curr TEXT, date TEXT, source TEXT, title TEXT, heading TEXT, sku TEXT, in_stock INTEGER, image TEXT, url TEXT);")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS prices_images (id INTEGER PRIMARY KEY AUTOINCREMENT, pid INTEGER, type INTEGER, path TEXT);")
        self.ADD_ITEM = "INSERT INTO prices_prices (pid, price, price_usd, curr, date, tmstamp, source, title, heading, sku, in_stock, image, url) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"
        self.CHK_ITEM = "SELECT * FROM prices_images WHERE pid = ?;"
        self.CHK_ITEM1 = "SELECT * FROM prices_prices WHERE pid = ? and date = ? and source = ?;"

    def spider_closed(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):

        self.types = {'full': 0, 'thumbs/normal': 1, 'thumbs/icon': 2}

        if self.CheckItemDBOneField(item['pid']):
            for k, v in self.types.iteritems():
                try:
                    self.cur.execute("INSERT INTO prices_images (pid,type,path) VALUES (?,?,?)",
                                     (
                                         item['pid'],
                                         v,
                                         k + item['image_paths'].replace('full', '')
                                     ))
                    self.conn.commit()
                except:
                    log.msg("Unable to store img " + str(item['image_paths']), log.ERROR, spider=spider)
                    log.msg(traceback.format_exc(), log.ERROR)

        for k in item.iterkeys():
            try:
                item[k] = unicodedata.normalize('NFKD', item[k]).encode('ascii', 'ignore')
            except:
                pass

        if self.CheckItemDBThreeFields(item['pid'], item['date'], item['source']):
            try:
                self.cur.execute(self.ADD_ITEM,
                                 (item['pid'],
                                  item['price'],
                                  item['price_usd'],
                                  item['curr'],
                                  item['date'],
                                  item['tmstamp'],
                                  item['source'],
                                  item['title'],
                                  item['heading'],
                                  item['sku'],
                                  item['in_stock'],
                                  item['image'],
                                  item['url'],
                                 ))
            except:
                log.msg("Unable to add Item " + str(item['title']), log.ERROR, spider=spider)
                log.msg(traceback.format_exc(), log.ERROR)
            self.conn.commit()
        else:
            log.msg(
                "Item with pid = '" + str(item['pid']) + "' for date = '" + str(item['date']) + "' source = '" + str(
                    item['source']) + "' skipped as duplicate", log.DEBUG, spider=spider)

        return item

    def CheckItemDBOneField(self, ID):
        self.cur.execute(self.CHK_ITEM, (str(ID),))
        if self.cur.fetchone() is None:
            return True
        return False

    def CheckItemDBThreeFields(self, ID1, ID2, ID3):
        self.cur.execute(self.CHK_ITEM1, (str(ID1), str(ID2), str(ID3),))
        if self.cur.fetchone() is None:
            return True
        return False