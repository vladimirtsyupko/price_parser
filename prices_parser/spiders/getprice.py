#! /usr/bin/python
#! -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector, Selector
from scrapy.item import Item
from scrapy.http import Response, Request
from scrapy.http import FormRequest
from scrapy.http.cookies import CookieJar
import re
from prices_parser.items import ParsedPriceItem
from scrapy import log, signals
from datetime import date, timedelta, datetime
import calendar
import MySQLdb
import sqlite3
from tinypanel.settings import MYSQL_USER_HOST, MYSQL_USER_LOGIN, MYSQL_USER_PASSWD, MYSQL_USER_DB, DB_USE, \
    SQLITE_PATH, GDRIVE_EMAIL, GDRIVE_PASS, GDRIVE_FILE, LOCATION
import gspread
import urllib2, urllib
from bs4 import BeautifulSoup

DEBUG_FLAG = True
DEBUG_FLAG = False


class PricesSpider(CrawlSpider):
    name = "getprice"
    sites = ['drugstore.com', 'walmart.com', 'amazon.com', 'amazon.co.uk', 'target.com', 'rakuten.com', 'staples.com',
             'misco.ch', 'vikingdirekt.ch', 'finance.yahoo.com']
    allowed_domains = ['http://www.' + '%s' % (site) for site in sites] + ['www.' + '%s' % (site) for site in sites] + [
        site for site in sites]
    handle_httpstatus_list = [404]
    curr_dict = {}


    def __init__(self):
        super(PricesSpider, self).__init__()

        if 'mysql' in DB_USE:
            self.conn = MySQLdb.connect(user=MYSQL_USER_LOGIN, passwd=MYSQL_USER_PASSWD, db=MYSQL_USER_DB, host=MYSQL_USER_HOST, charset="utf8", use_unicode=True)
            self.cur = self.conn.cursor()
        elif 'sqlite' in DB_USE:
            self.conn = sqlite3.connect(SQLITE_PATH)
            self.cur = self.conn.cursor()


        # here we'll save all shops to dict {url: id}
        self.available_shops = {}
        self.start_urls = []
        self.start_urls_dict = {}
        self.titles_dict = {}
        self.curr_dict = self.get_currencies(urllib2.urlopen('http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote', timeout=10).read())

        # if 'mysql' in DB_USE:
        #     #self.cur.execute("CREATE TABLE IF NOT EXISTS prices_inputs (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), pid INT, url VARCHAR(255), active TINYINT(1));")
        #     pass
        # elif 'sqlite' in DB_USE:
        #     #conn.execute("""INSERT INTO prices_inputs (id, url, active) VALUES (1,"http://www.walmart.com/ip/Philips-Sonicare-Essence-E5300-Power-Toothbrush-HX5610-01/21264316",1);""")
        #     #conn.execute("""INSERT INTO prices_inputs (id, url, active) VALUES (1,"http://www.amazon.com/Philips-HX6511-50-Rechargeable-Toothbrush/dp/B004M1BO3U/ref=sr_1_1?ie=UTF8&amp;qid=1384281679&amp;sr=8-1&amp;keywords=sonicare+easy+clean",1);""")
        #     #conn.execute("""INSERT INTO prices_inputs (id, url, active) VALUES (1,"http://www.drugstore.com/philips-sonicare-easy-clean-sonic-toothbrush-hx6511/qxp344199?catid=186720",1);""")
        #     #self.conn.execute("CREATE TABLE IF NOT EXISTS prices_inputs (id INTEGER PRIMARY KEY AUTOINCREMENT, pid INTEGER, url TEXT, title TEXT, active INTEGER);")
        #     pass

        if 'mysql' in DB_USE or 'sqlite' in DB_USE:
            self.conn.commit()
            self.cur.execute("""
                SELECT s.id, s.url
                FROM price_parser_shop s;
            """)
            self.inputs = self.cur.fetchall()
            for row in self.inputs:
                self.available_shops[row[1]] = row[0]
            self.cur.execute("""
                SELECT s.url, sku.product_id , sku.sku, s.id
                FROM price_parser_product_sku sku
                INNER JOIN price_parser_product p on p.id=sku.product_id
                INNER JOIN price_parser_shop s on s.id=sku.shop_id
                WHERE p.active = 1;
            """)
            self.conn.commit()
            self.inputs = self.cur.fetchall()
            # self.start_urls = [u[0].encode('utf8') for u in self.inputs]
            for row in self.inputs:
                self.generate_parse_link(row[0], row[1], row[2])

        elif 'gdrive' in DB_USE:
            gc = gspread.login(GDRIVE_EMAIL, GDRIVE_PASS)
            wks = gc.open(GDRIVE_FILE).sheet1
            #all_data = wks.get_all_values()
            for row in wks.get_all_values()[1:]:
                if row[0]:  # skip blank pids
                    pid_ = row[0]
                    title_ = row[1]
                    if not DEBUG_FLAG:
                        if row[3]:  # amazon.com and amazon.co.uk id
                            url_ = 'http://www.amazon.com/dp/'+str(row[3])
                            self.start_urls.append(url_)
                            self.start_urls_dict.update({url_: pid_})  # url vs pid
                            self.titles_dict.update({pid_: title_})     # pid vs title

                            url_ = 'http://www.amazon.co.uk/dp/'+str(row[3])
                            self.start_urls.append(url_)
                            self.start_urls_dict.update({url_: pid_})  # url vs pid
                            self.titles_dict.update({pid_: title_})     # pid vs title

                        if row[6]:  # staples.com
                            url_ = 'http://www.staples.com/office/supplies/StaplesZipCodeAdd?zipCode='+LOCATION+'&storeId='+LOCATION+'&langId=-1&URL=StaplesProductDisplay%3FcatalogIdentifier%3D2%26langId%3D%252d1%26storeId%3D'+LOCATION+'%26partNumber%3D'+str(row[6])+'&errorUrl=zipcode'
                            self.start_urls.append(url_)
                            self.start_urls_dict.update({'http://www.staples.com/office/supplies/StaplesProductDisplay?storeId='+LOCATION+'&partNumber='+str(row[6])+'&catalogIdentifier=2&langId=-1&ddkey=http:StaplesZipCodeAdd':pid_}) # url vs pid
                            self.titles_dict.update({pid_: title_})     # pid vs title

                        if row[7]:  # Misco No
                            url_ = 'http://www.misco.ch/product/' + str(row[7])
                            self.start_urls.append(url_)
                            self.start_urls_dict.update({url_: pid_})  # url vs pid
                            self.titles_dict.update({pid_: title_})     # pid vs title

                        if row[8]:  # walmart id
                            url_ = 'http://www.walmart.com/ip/' + str(row[8])
                            self.start_urls.append(url_)
                            self.start_urls_dict.update({url_: pid_})  # url vs pid
                            self.titles_dict.update({pid_: title_})     # pid vs title
                    else:  # DEBUG_FLAG=True
                        if row[3]:
                            url_ = 'http://www.amazon.co.uk/dp/' + str(row[3])
                            self.start_urls.append(url_)
                            self.start_urls_dict.update({url_: pid_})  # url vs pid
                            self.titles_dict.update({pid_: title_})     # pid vs title

        log.msg("It's going to process " + str(len(self.start_urls)) + " active input urls", log.DEBUG)
        log.msg("list of urls ***" + str(self.start_urls) + "***", log.DEBUG)


    def generate_parse_link(self, shop_url, product_id, sku):
        """
        This function will generate link for product page by given
        shop url and product sku, and append it to the self.start_urls .
        And also associate links with product ids
        """
        if 'amazon.com' == shop_url or 'amazon.co.uk' == shop_url:
            shop_id = self.available_shops.get('amazon.com', False)
            if shop_id:
                url_ = 'http://www.amazon.com/dp/'+str(sku)
                self.start_urls.append(url_)
                self.start_urls_dict.update({url_: (product_id, shop_id)})  # url vs pid

            shop_id = self.available_shops.get('amazon.co.uk', False)
            if shop_id:
                url_ = 'http://www.amazon.co.uk/dp/'+str(sku)
                self.start_urls.append(url_)
                self.start_urls_dict.update({url_: (product_id, shop_id)})  # url vs pid

        elif 'target.com' == shop_url:
            pass
            # shop_id = self.available_shops.get(shop_url, False)
            # if shop_id:
            #     url_ = 'http://www.misco.ch/product/'+str(sku)
            #     self.start_urls.append(url_)
            #     self.start_urls_dict.update({url_: (product_id, shop_id)})  # url vs pid
        elif 'rakuten.com' == shop_url:
            pass
        elif 'drugstore.com' == shop_url:
            pass
        elif 'walmart.com' == shop_url:
            shop_id = self.available_shops.get(shop_url, False)
            if shop_id:
                url_ = 'http://www.walmart.com/ip/'+str(sku)
                self.start_urls.append(url_)
                self.start_urls_dict.update({url_: (product_id, shop_id)})  # url vs pid
        elif 'misco.ch' == shop_url:
            shop_id = self.available_shops.get(shop_url, False)
            if shop_id:
                url_ = 'http://www.misco.ch/product/'+str(sku)
                self.start_urls.append(url_)
                self.start_urls_dict.update({url_: (product_id, shop_id)})  # url vs pid
        elif 'staples.com' == shop_url:  # hold on with this site, need additional investigation of post data
            shop_id = self.available_shops.get(shop_url, False)
            if shop_id:
                url_ = 'http://www.staples.com/office/supplies/StaplesZipCodeAdd?zipCode='+LOCATION+'&storeId='+LOCATION\
                       +'&langId=-1&URL=StaplesProductDisplay%3FcatalogIdentifier%3D2%26langId%3D%252d1%26storeId%3D'+\
                       LOCATION+'%26partNumber%3D'+str(sku)+'&errorUrl=zipcode'
                self.start_urls.append(url_)
                self.start_urls_dict.update({url_: (product_id, shop_id)})  # url vs pid

        elif 'vikingdirekt.ch' == shop_url:  # hold on with this site, need additional investigation of post data
            pass

    def curr_from_price(self, txt):
        if u'\xa3' in txt:
            return u'GBP'
        elif u'$' in txt:
            return u'USD'
        elif u'Fr.' in txt or u'CHF' in txt:
            return u'CHF'

    def usd_from_price(self, pr, cur):
        if u'USD' in cur:
            return pr
        else:
            return "{0:.2f}".format(float(pr) / self.curr_dict[cur])

    def _process_url(self, item, response, hxs):

        if 'amazon.com' in response.url:
            return self._parse_amazon_com(item, response, hxs)
        elif 'amazon.co.uk' in response.url:
            return self._parse_amazon_co_uk(item, response, hxs)
        elif 'target.com' in response.url:
            return self._parse_target_com(item, response, hxs)
        elif 'rakuten.com' in response.url:
            return self._parse_rakuten_com(item, response, hxs)
        elif 'drugstore.com' in response.url:
            return self._parse_drugstore_com(item, response, hxs)
        elif 'walmart.com' in response.url:
            return self._parse_walmart_com(item, response, hxs)
        elif 'misco.ch' in response.url:
            return self._parse_misco_ch(item, response, hxs)
        elif 'staples.com' in response.url:  # hold on with this site, need additional investigation of post data
            return self._parse_staples_com(item, response, hxs)
        elif 'vikingdirekt.ch' in response.url:  # hold on with this site, need additional investigation of post data
            return self._parse_vikingdirekt_ch(item, response, hxs)

    def parse_start_url(self, response):
        item = ParsedPriceItem()
        hxs = Selector(response)

        if response.status == 404:
            # item['source'] = 'Page unavailable [404]'
            # item['heading'] = 'Page unavailable [404]'
            # # item['sku'] = 'Page unavailable [404]'
            # item['in_stock'] = False
            # item['image'] = 'Page unavailable [404]'
            # item['price'] = 0
            # item['currency'] = ''
            return None
        else:
            item = self._process_url(item, response, hxs)

        try:
            item['price_usd'] = self.usd_from_price(item['price'], item['currency'])
        except:
            item['price_usd'] = 0

        item['url'] = response.request.url

        # item['date'] = str(date.today())
        item['when_created'] = datetime.now()

        try:
            item['shop_id'] = self.start_urls_dict[response.request.url][1]
        except:
            item['shop_id'] = None
        try:
            item['product_id'] = self.start_urls_dict[response.request.url][0]
        except:
            item['product_id'] = None

        # print item
        return item


    def get_currencies(self, body):
        soup = BeautifulSoup(body)
        tmp = {}
        for x in soup.findAll('resource'):
            if 'USD' in x.find('field', {'name': 'name'}).text:
                tmp.update({
                x.find('field', {'name': 'name'}).text.split('/')[-1]: float(x.find('field', {'name': 'price'}).text)})
        return tmp

    def _parse_amazon_com(self, item, response, hxs):
        item['source'] = u'amazon.com'
        # try:
        #     item['sku'] = re.compile(r'/([A-Z0-9]+)/{0,}').findall(response.url)[0]
        # except:
        #     item['sku'] = None
        try:
            item['in_stock'] = u'in stock' in hxs.xpath('//span[@class="availGreen"]/text()')[0].extract().lower() \
                or u'available from' in hxs.xpath('//span[@class="availGreen"]/text()')[0].extract().lower()
        except:
            try:
                item['in_stock'] = u'in stock' in hxs.xpath('//div[@id="availability"]/span/text()')[0].extract().lower() \
                    or u'available from' in hxs.xpath('//div[@id="availability"]/span/text()')[0].extract().lower()
            except:
                item['in_stock'] = False
        try:
            item['image'] = hxs.xpath('//img[@id="main-image"]/@src')[0].extract()
        except:
            try:
                item['image'] = hxs.xpath('//div[@id="rwImages_hidden"]/img/@src')[0].extract()
            except:
                try:
                    # this is actually a last resort
                    dirty_data = hxs.xpath('//img[@id="landingImage"]/@data-a-dynamic-image')[0].extract()
                    clean_path = dirty_data.split(u'":[')[0].replace(u'{"', u'')
                    item['image'] = clean_path
                except:
                    item['image'] = None
        try:
            item['heading'] = hxs.xpath('//span[@id="productTitle"]/text()')[0].extract().strip()
        except:
            try:
                item['heading'] = hxs.xpath('//span[@id="btAsinTitle"]/text()')[0].extract().strip()
            except:
                try:
                    item['heading'] = hxs.xpath('//div[@id="title_feature_div"]/div/h1/text()')[0].extract().strip()
                except:
                    item['heading'] = None
        try:
            item['price'] = hxs.xpath('//span[@id="priceblock_ourprice"]/text()').re('\d+\.\d+')[0]
            item['currency'] = self.curr_from_price(hxs.xpath('//span[@id="priceblock_ourprice"]/text()').extract()[0])
        except:
            try:
                item['price'] = hxs.xpath('//*[@class="priceLarge"]/text()').re('\d+\.\d+')[0]
                item['currency'] = self.curr_from_price(hxs.xpath('//*[@class="priceLarge"]/text()').extract()[0])
            except:
                try:
                    item['price'] = hxs.xpath('//[@class="priceLarge"][1]/text()').re('\d+\.\d+')[0]
                    item['currency'] = self.curr_from_price(hxs.xpath('//*[@class="priceLarge"]/text()').extract()[0])
                except:
                    try:
                        item['price'] = hxs.xpath('//span[@class="price"]/text()').re('\d+\.\d+')[0]
                        item['currency'] = self.curr_from_price(hxs.xpath('//span[@class="price"]/text()').extract()[0])
                    except:
                        try:
                            item['price'] = hxs.xpath('//span[@id="listPriceValue"]/text()').re('\d+\.\d+')[0]
                            item['currency'] = self.curr_from_price(hxs.xpath('//span[@id="listPriceValue"]/text()').extract()[0])
                        except:
                            item['price'] = 0
                            item['currency'] = ''
        return item

    def _parse_amazon_co_uk(self, item, response, hxs):
        if 'amazon.co.uk' in response.url:
            item['source'] = u'amazon.co.uk'
            # try:
            #     item['sku'] = re.compile(r'/([A-Z0-9]+)/{0,}').findall(response.url)[0]
            # except:
            #     item['sku'] = None
            try:
                item['in_stock'] = u'in stock' in hxs.xpath('//span[@class="availGreen"]/text()')[
                    0].extract().lower() or u'available from' in hxs.xpath('//span[@class="availGreen"]/text()')[
                                       0].extract().lower()
            except:
                item['in_stock'] = False
            try:
                item['image'] = hxs.xpath('//img[@id="main-image"]/@src')[0].extract()
            except:
                item['image'] = None
            try:
                item['heading'] = hxs.xpath('//div[@id="buying"]/h1[@class="parseasinTitle"]/span/span/text()')[
                    0].extract().strip()
            except:
                try:
                    item['heading'] = hxs.xpath('//span[@id="btAsinTitle"]/span/text()')[0].extract().strip()
                except:
                    item['heading'] = None
            try:
                tag = hxs.xpath('//span[@id="priceblock_ourprice"]/text()')
                item['price'] = tag.re('\d+\.\d+')[0]
                item['currency'] = self.curr_from_price(tag.extract()[0])
            except:
                try:
                    tag = hxs.xpath('//*[@class="priceLarge"]/text()')
                    item['price'] = tag.re('\d+\.\d+')[0]
                    item['currency'] = self.curr_from_price(tag.extract()[0])
                except:
                    try:
                        tag = hxs.xpath('//span[@id="listPriceValue"]/text()')
                        item['price'] = tag.re('\d+\.\d+')[0]
                        item['currency'] = self.curr_from_price(tag.extract()[0])
                    except:
                        try:
                            tag = hxs.xpath('//span[@class="price"]/text()')
                            item['price'] = tag.re('\d+\.\d+')[0]
                            item['currency'] = self.curr_from_price(tag.extract()[0])
                        except:
                            item['price'] = 0
                            item['currency'] = ''
        return item

    def _parse_target_com(self, item, response, hxs):
        item['source'] = u'target.com'
        try:
            item['heading'] = hxs.xpath('//h1[@class="captionText"]/text()')[0].extract().strip()
        except:
            item['heading'] = None
        try:
            tag = hxs.xpath('//div[@id="OldPriceForUnavailableProductDiv"]/span/text()')
            item['price'] = tag.re('\d+\.\d+')[0]
            item['currency'] = self.curr_from_price(tag.extract()[0])
        except:
            item['price'] = 0
            item['currency'] = ''
        return item

    def _parse_rakuten_com(self, item, response, hxs):
        item['source'] = u'rakuten.com'
        # try:
        #     item['sku'] = response.url.split('/')[-1].split('.')[0]
        # except:
        #     item['sku'] = None
        try:
            item['in_stock'] = u'in stock' in hxs.xpath('//span[@id="spanStockStatus"]/text()')[0].extract().lower()
        except:
            item['in_stock'] = False
        try:
            item['image'] = hxs.xpath('//div[@class="item image"]/@data-buyzoom')[0].extract().split('"')[-2]
        except:
            item['image'] = None
        try:
            item['heading'] = hxs.xpath('//a[@name="productTitle"]/text()')[0].extract().strip()
        except:
            item['heading'] = None
        try:
            tag = hxs.xpath('//span[@id="spanMainTotalPrice"]/text()')
            item['price'] = tag.re('\d+\.\d+')[0]
            item['currency'] = self.curr_from_price(tag.extract()[0])
        except:
            item['price'] = 0
            item['currency'] = ''
        return item

    def _parse_drugstore_com(self, item, response, hxs):
        item['source'] = u'drugstore'
        # try:
        #     item['sku'] = response.url.split('?catid=')[-1].split('&')[0]
        # except:
        #     item['sku'] = None
        try:
            item['in_stock'] = u'in stock' in hxs.xpath('//div[@id="divAvailablity"]/text()')[0].extract().lower()
        except:
            item['in_stock'] = False
        try:
            item['image'] = 'http://www.drugstore.com' + hxs.xpath('//div[@id="largeProdImageLink"]/a/@href')[0].extract().split("'")[1]
        except:
            item['image'] = None
        try:
            item['heading'] = hxs.xpath('//h1[@class="captionText"]/text()')[0].extract().strip()
        except:
            item['heading'] = None
        try:
            tag = hxs.xpath('//div[@id="OldPriceForUnavailableProductDiv"]/span/text()')
            item['price'] = tag.re('\d+\.\d+')[0]
            item['currency'] = self.curr_from_price(tag.extract()[0])
        except:
            try:
                tag = hxs.xpath('//div[@id="productprice"]/b/text()')
                item['price'] = tag.re('\d+\.\d+')[0]
                item['currency'] = self.curr_from_price(tag.extract()[0])
            except:
                item['price'] = 0
                item['currency'] = ''
        return item

    def _parse_walmart_com(self, item, response, hxs):
        item['source'] = u'walmart.com'
        # try:
        #     item['sku'] = response.url.split('/')[-1]
        # except:
        #     item['sku'] = None
        try:
            item['in_stock'] = u'in stock' in hxs.xpath('//span[@class="BodyLBoldGreen"]/text()')[0].extract().lower()
        except:
            item['in_stock'] = False
        try:
            item['image'] = hxs.xpath('//div[contains(@class,"LargeItemPhoto")]/a/@href')[0].extract()
        except:
            item['image'] = None
        try:
            item['heading'] = hxs.xpath('//h1[@class="productTitle"]/text()')[0].extract().strip()
        except:
            item['heading'] = None
        try:
            item['price'] = hxs.xpath('//span[contains(@class,"camelPrice")]/span[contains(@class,"bigPriceText")]/text()').re('\d+')[0] + '.' + hxs.xpath('//span[contains(@class,"camelPrice")]/span[contains(@class,"smallPriceText")]/text()').re('\d+')[0]
            item['currency'] = self.curr_from_price(hxs.xpath('//span[contains(@class,"camelPrice")]/span[@class="bigPriceText1"]/text()').extract()[0])
        except:
            item['price'] = 0
            item['currency'] = ''
        return item

    def _parse_misco_ch(self, item, response, hxs):
        item['source'] = u'misco.ch'

        #unavailable
        if u'entschuldigung, das produkt ist aktuell nicht verf\xfcgbar' in hxs.xpath('//span[@class="error size14 b"]/text()')[0].extract().lower():
            # item['sku'] = 'Product unavailable'
            item['in_stock'] = False
            item['image'] = 'Product unavailable'
            item['heading'] = 'Product unavailable'
            item['price'] = 0
            item['currency'] = ''
        else:
            # try:
            #     #item['sku'] = response.url.split('/')[-1]
            #     item['sku'] = hxs.xpath('//div[@id="MiscoNumber"]/text()')[0].extract().split(':')[-1].strip()
            # except:
            #     item['sku'] = None
            try:
                item['in_stock'] = u'ab lager sofort verf\xfcgbar' in hxs.xpath('//div[@style="margin-bottom: 6px;"]/b/text()')[0].extract().lower()
            except:
                item['in_stock'] = False
            try:
                item['image'] = hxs.xpath('//div[@id="zoomImage"]/a/@href')[0].extract()
            except:
                item['image'] = None
            try:
                item['heading'] = hxs.xpath('//div[@class="size12 b ProductInfoDescription"]/h1/text()')[0].extract().strip()
            except:
                item['heading'] = None
            try:
                #tag = hxs.xpath('//tr[@class="borderless"]/td[1][contains(text(),"Preis:")]/following-sibling::td/span[@class="size20 b"]/text()')
                tag = hxs.xpath('//span[@class="size20 b"]/text()')
                item['price'] = tag.re('\d+\.\d+')[0]
                item['currency'] = self.curr_from_price(tag.extract()[0])
            except:
                item['price'] = 0
                item['currency'] = ''

        return item

    def _parse_staples_com(self, item, response, hxs):
        item['source'] = u'staples.com'
        if u'page not found' in ''.join(hxs.xpath('//div[@class="content"]/h1/text()').extract()).lower():
            # item['sku'] = 'Product unavailable'
            item['in_stock'] = False
            item['image'] = 'Product unavailable'
            item['heading'] = 'Product unavailable'
            item['price'] = 0
            item['currency'] = ''
        else:
            # try:
            #     item['sku'] = response.url.split('partNumber=')[-1].split('&')[0]
            # except:
            #     item['sku'] = None
            try:
                item['in_stock'] = u'in stock online' in hxs.xpath('//li[contains(@class,"instockonline")]/text()')[0].extract().lower()
            except:
                item['in_stock'] = False
            try:
                item['image'] = hxs.xpath('//img[@id="largeProductImage"]/@src')[0].extract()
            except:
                item['image'] = None
            try:
                item['heading'] = hxs.xpath('//div[contains(@class,"productDetails")]/h1/text()')[0].extract().strip()
            except:
                item['heading'] = None
            try:
                tag = hxs.xpath('//*[@class="finalPrice"]')
                item['price'] = tag.re('\d+\.\d+')[0]
                item['currency'] = self.curr_from_price(tag.extract()[0])
            except:
                item['price'] = 0
                item['currency'] = ''
        return item

    def _parse_vikingdirekt_ch(self, item, response, hxs):
        item['source'] = u'vikingdirekt.ch'
        # try:
        #     item['sku'] = hxs.xpath('//div[@id="skuHeading"]/div[@class="item_sku"]/text()')[0].extract().split('Artikel-Nr.')[-1].strip()
        # except:
        #     item['sku'] = None
        try:
            item['in_stock'] = u'verf\xfcgbar' in hxs.xpath('//table[@class="hBreaks hBreaksComponent"]/tr/td/span[@class="vkg_avail_sku"]/text()')[0].extract().lower()
        except:
            item['in_stock'] = False
        try:
            item['image'] = hxs.xpath('//div[@class="product_image photo"]/img/@src')[0].extract()
        except:
            item['image'] = None
        try:
            item['heading'] = hxs.xpath('//div[@id="skuHeading"]/h1/text()')[0].extract().strip()
        except:
            item['heading'] = None
        try:
            tag = hxs.xpath('//td[@id="priceNoTax0"]/text()')
            item['price'] = tag.re('\d+\.\d+')[0]
            item['currency'] = self.curr_from_price(tag.extract()[0])
        except:
            item['price'] = 0
            item['currency'] = ''

        return item