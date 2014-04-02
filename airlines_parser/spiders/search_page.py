import json
import datetime
import dateutil
from dateutil.relativedelta import relativedelta
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
import time
from airlines_parser.functions import html_to_clean_text, safe_list_get
from airlines_parser.models import ParsedFlight, Seat, Cookie, Flight

today = datetime.date.today()
nextmonth = datetime.date.today() + relativedelta(months=1)

PARSE_SETTINGS = {
    'originAirport': 'JFK',
    'destinationAirport': 'LHR',
    'travelMonth': str(today.month),
    'travelDay': str(today.day),
    'nextMonth': str(nextmonth.month),
    'nextMonthDay': str(nextmonth.day),
    'tripType': 'oneWay',
    'adultPassengerCount': '1',
    'childPassengerCount': '0',
    'flightNumber': '100',
    # TODO CHANGE
    'departureDate': time.strftime('%m/%d/%Y'),
    # 'cabin': {'coach', 'business', 'first'}
    'cabin': 'coach',
}


class AirlinesSpider(Spider):

    def log_message(self, message):
        with open("log.txt", "a") as myfile:
            myfile.write('[%s]:[%s]\n' % (datetime.datetime.now(), message))

    today = datetime.date.today()
    nextmonth = today + relativedelta(weeks=1)
    PARSE_SETTINGS = {
        'originAirport': 'JFK',
        'destinationAirport': 'LHR',
        'travelMonth': str(today.month),
        'travelDay': str(today.day),
        'nextMonth': str(nextmonth.month),
        'nextMonthDay': str(nextmonth.day),
        'tripType': 'oneWay',
        'adultPassengerCount': '1',
        'childPassengerCount': '0',
        'flightNumber': '100',
        # TODO CHANGE
        'departureDate': time.strftime('%m/%d/%Y'),
        # 'cabin': {'coach', 'business', 'first'}
        'cabin': 'coach',
    }

    cookies = {
        'APISID': 'J_uYyKfHBz0TxuHE/ApZi9O1KupSN11OTK',
        # 'GOOGLE_ABUSE_EXEMPTION': 'ID=6d85ae157d784af7:TM=1394727292:C=c:IP=195.69.186.61-:S=APGng0voLAoaD0S0SbXloepXQCyqrqRRpw',
        'HSID': 'AYNN-TqPjsPU5jf-_',
        # 'JSESSIONID': 'CA2A1907E5FC869634F0134FE279DCF1',
        # 'NID': '67=QZf2rRdTerEveSI1Xt6MBbW91OUUbxCyLUPacSs4B_CnQl1R_FdWR56jJgtzia39SzAeb8y9hSlf3a7JtmqwrtkrREVzoEzMiDWGpgxSi3ymLn_wj5UOQTyiU1NxfF4YwCtp38keZtzahsDSFcFFKrSA91tBz1z4V',
        'OX_plg': 'swf|qt|wmp|shk|pm',
        'PREF': 'ID=3ac12603b8930d08:U=7bdfd257d13de9f7:FF=4:LD=ru:TM=1389195024:LM=1393932115:GM=1:S=7fnyJbvmMxOS45Gb',
        'ROUTEID': '.P106B05',
        'MUID': '2D63B8EF5100620E2B31BD5052006219',
        'SAPISID': 'VsoQ4FgUuigCJrr9/AgdnmVkZxcdK9zwoy',
        # 'SID': 'DQAAAP0BAABRj9PDWjc71w7bx5qMv1rFWKSMpyyQhbDNjgtOSvrJi9JNH2N_7RdEd4rr6yr1gjys-lWtjaoFoyNuv_3wGWhJv5w_Hx_nRGv7q5IxHEln80u1u7Ux0XWh5I6CJ8NXbp4Fb6k5-Ds-',
        'SSID': 'A7Oj-9Djk9ySJPyzx',
        'BC_BANDWIDTH': '1395071372782X2927',
        # 'COUNTRY_CODE': '"OEpYVVx9wMg="',
        'aawaScreenRes': 'done',
        'dtCookie': '6AC407A78803F3ECD8DA11500A2F86BE|AA.com|1',
        'dtLatC': '114|113|118|110|111|116|119.5|114.5|118|115.5|112.5',
        'dtPC': '-',
        'v1st': '6F6C7C60137C5BF0',
        'id': '221ffac9c501006c||t=1389185856|et=730|cs=002213fd48c40e01fc98fbc997',
        'departureDateCookie': time.strftime('%m/%d/%Y'),
        'sessionLocale': 'en_US',
        'locale': 'en_US',
    }

    allowed_domains = [
        ".www.aa.com",
        "www.aa.com",
        '.aa.com'
    ]


class ParseCookiesSpider(AirlinesSpider):
    """
    Parser for price and flightNumber
    """
    name = "parse_cookies"

    start_urls = [
        # "https://www.aa.com/homePage.do",
        "https://www.aa.com/reservation/searchFlightsSubmit.do",
    ]

    def start_requests(self):
        #refresh cookie keys each 15 minutes
        allowed_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
        cookie = Cookie.objects.filter(when_created__gte=allowed_time)
        if not cookie:
            #  if our cookies not fresh enough make'em fresh
            return [FormRequest(
                url=self.start_urls[0],
                method='POST',
                cookies=self.cookies,
                formdata={
                    'originAirport': PARSE_SETTINGS['originAirport'],
                    'destinationAirport': PARSE_SETTINGS['destinationAirport'],
                    'flightParams.flightDateParams.travelMonth': PARSE_SETTINGS['travelMonth'],
                    'flightParams.flightDateParams.travelDate': PARSE_SETTINGS['travelDay'],
                    'adultPassengerCount': PARSE_SETTINGS['adultPassengerCount'],
                    'childPassengerCount': PARSE_SETTINGS['childPassengerCount'],
                    'flightParams.flightDateParams.searchTime': "120001",
                    'currentCalForm': 'dep',
                    'tripType': 'oneWay',
                    },
                callback=self.first_callback,
            )]
        else:
            #otherwise do nothing
            return []

    def first_callback(self, response):
        """
        In the first callback we'll take the cookies, that will be generated for us by webpage
        in order to access pages with needed info
        """
        cookie = Cookie.objects.create(
            cookie_keys=json.dumps(response.headers.getlist('Set-Cookie'))
        )
        cookie.save()
        print '-/-*-/Cookie saved successfully/-*-/ --- @:=D'


class ParsePriceSpider(AirlinesSpider):
    """
    Parser for price and flightNumber
    """
    name = "parse_price"
    start_urls = [
        "https://www.aa.com/reservation/searchFlightsSubmit.do",
    ]

    def __init__(self, flight_id=1, departure_date=str(datetime.date.today()), monthly=0):
        # flag which tells us if this a monthly parsed info or regular
        self.monthly = monthly
        try:
            # first of all we'll take cookies from step one
            db_cookies = Cookie.objects.order_by('-when_created')[0]
            for cookie_string in json.loads(db_cookies.cookie_keys):
                cookie_values = safe_list_get(cookie_string.split(u';'), 0)
                cookie_key = safe_list_get(cookie_values.split(u'='), 0)
                cookie_value = u'='.join(cookie_values.split(u'=')[1:])
                self.cookies[cookie_key] = cookie_value
        except Cookie.DoesNotExist:
            self.log_message("ERROR: There's no cookies from step one!")
        try:
            self.flight = Flight.objects.get(pk=flight_id)
        except Flight.DoesNotExist:
            self.log_message("ERROR: There's no flight with such id!")
        # then change parameters, if needed
        today = datetime.datetime.strptime(departure_date, "%Y-%m-%d").date()
        nextmonth = today + relativedelta(days=7)
        self.PARSE_SETTINGS = {
            'originAirport': self.flight.origin,
            'destinationAirport': self.flight.destination,
            'travelMonth': str(today.month),
            'travelDay': str(today.day),
            'nextMonth': str(nextmonth.month),
            'nextMonthDay': str(nextmonth.day),
            'tripType': 'oneWay',
            'adultPassengerCount': '1',
            'childPassengerCount': '0',
            'flightNumber': self.flight.flight_number,
            'departureDate': departure_date,
        }


    def start_requests(self):
        return [FormRequest(
            url=self.start_urls[0],
            method='POST',
            cookies=self.cookies,
            formdata={
                'dateChanged': '',
                'flightSearch': 'revenue',
                'tripType': 'oneWay',  # in your face BIATCH!!!
                'fromSearchPage': 'true',
                'searchCategory': 'false',
                'netSaaversTripType': '',
                'aairpassSearchType': 'false',
                'air_room_car': 'A',
                'aavDeepLinkUrl': 'http://www.aavacations.com/deeplink.asp',
                'currentCodeForm': '',
                'originAirport': self.PARSE_SETTINGS['originAirport'],
                'destinationAirport': self.PARSE_SETTINGS['destinationAirport'],
                'originAlternateAirportDistance': '0',
                'destinationAlternateAirportDistance': '0',
                'searchType': 'matrix',
                'numberOfStopsMatrix': 'P',
                'numberOfStopsSchedule': 'P',
                'numberOfFlightsToDisplay': '1000',
                'currentCalForm': 'dep',
                'flightParams.flightDateParams.travelMonth': self.PARSE_SETTINGS['travelMonth'],
                'flightParams.flightDateParams.travelDay': self.PARSE_SETTINGS['travelDay'],
                'flightParams.flightDateParams.searchTime': '120001',
                'returnDate.travelMonth': self.PARSE_SETTINGS['nextMonth'],
                'returnDate.travelDay': self.PARSE_SETTINGS['nextMonthDay'],
                'returnDate.searchTime': '040001',
                'adults': '1',
                'rooms': '1',
                'serviceclass': 'coach',
                'adultPassengerCount': self.PARSE_SETTINGS['adultPassengerCount'],
                'seniorPassengerCount': '0',
                'youngAdultPassengerCount': '0',
                'childPassengerCount': '0',
                'infantPassengerCount': '0',
                'classOfServicePreference': 'coach-restricted',
                'cabinOfServicePreference': 'matrix-lowest_fare',
                'cabinOfServicePreference': 'matrix-show_all',
                'carrierPreference': 'T',
                'countryPointOfSale': 'US',
                'm_recaptcha_challenge_field': '03AHJ_VuvDrOndV65ogcWsvpFkm-VZUjIzC6ShkAFRHc9792qjZUocYrsNEhOP_4WzErsYQrHNTJifNbn-Q7B-QolXf3hgw6DgqQTKMKAlSmUWT_OooPNhvItug0y8ezczBwLpeog4OTzxhacKxNSUsW05Cp1n1o7a9u0VALx7dwpBY4nr4fP56IirxZ8XxS7djfiU74pnpNPzOtP4X5paXZmmw18xqRO3C6uFjqhfjcOWfvLNG8STe8qPKlpVtKSyQYrEw82E8efQDCoCTBGKYQmQyChzI9zs0Q',
                'passengerCount': '1',
                '_button_success': 'Continue',
                },
            callback=self.second_callback,
        )]

    def clean_price(self, price):
        if price == '999999999999999999':
            return 0
        else:
            return price

    def second_callback(self, response):
        """
        In the second callback we'll be saving flight info
        """
        # filename = response.url.split("/")[-2] + '.html'
        # open(filename, 'wb').write(response.body)
        sel = Selector(response)
        #  this is basically <tr> that contains all needed info
        info_container = sel.xpath("//span[contains(@class,'aa-flight-number') and contains(text(),'"+self.PARSE_SETTINGS['flightNumber']+"\n')]/ancestor::tr[contains(@class,'row-vm segment-first')]")
        if not info_container:
            # if there's a link in tr instead of span info container will be empty
            # if this happens we'll try to find again with the link
            info_container = sel.xpath("//span[contains(@class,'aa-flight-number')]/a[text()='"+self.PARSE_SETTINGS['flightNumber']+"']/ancestor::tr[contains(@class,'row-vm segment-first')]")
        try:
            departure = html_to_clean_text(info_container.xpath(".//td[contains(@class,'aa-flight-time')][1]/strong").extract()[0])
            arrival = html_to_clean_text(info_container.xpath(".//td[contains(@class,'aa-flight-time')][2]/strong").extract()[0])
            # saving prices to an array
            prices = map(lambda x: self.clean_price(html_to_clean_text(x)), info_container.xpath(".//div[contains(@class,'faresort')]").extract())
            fares = map(lambda x: self.clean_price(html_to_clean_text(x)), sel.xpath("//th[contains(@class,'fare-column')]").extract())
        except IndexError:
            self.log_message('ERROR There"s an error occurred while parsing html/Please check the generated html-files!')
        #  check for existence
        flight, created = ParsedFlight.objects.get_or_create(
            flight=self.flight,
            departure_date=self.PARSE_SETTINGS['departureDate'],
            monthly=self.monthly,
            defaults={
                'departure': departure,
                'arrival': arrival,
                'monthly': self.monthly,
                'prices': json.dumps(dict(zip(fares, prices)))}
        )
        if created:
            self.log_message('-*-*-New ParsedFlight #%s added!-*-*-' % self.PARSE_SETTINGS['flightNumber'])
        else:
            self.log_message('-*-*-ParsedFlight #%s updated!-*-*-' % self.PARSE_SETTINGS['flightNumber'])


class ParseAvailableSeatsSpider(AirlinesSpider):
    """
    Parser for getting available seats by params
    """
    name = "parse_available_seats"
    allowed_domains = [".www.aa.com",
                       "www.aa.com",
                       '.aa.com'
    ]
    start_urls = [
        "https://www.aa.com/seatmap/viewSeatsSubmit.do"
    ]

    CABIN_CHOICES = (
        'first', 'business', 'coach'
    )

    seat_legend = {}

    def __init__(self, flight_id=1, departure_date=datetime.datetime.today(), monthly=0):
        self.monthly = monthly
        try:
            # first of all we'll take cookies from step one
            db_cookies = Cookie.objects.order_by('-when_created')[0]
            for cookie_string in json.loads(db_cookies.cookie_keys):
                cookie_values = safe_list_get(cookie_string.split(u';'), 0)
                cookie_key = safe_list_get(cookie_values.split(u'='), 0)
                cookie_value = u'='.join(cookie_values.split(u'=')[1:])
                self.cookies[cookie_key] = cookie_value
                # print cookie_key, cookie_value
        except Cookie.DoesNotExist:
            self.log_message("ERROR: There's no cookies from step one!")
        try:
            self.flight = Flight.objects.get(pk=flight_id)
        except Flight.DoesNotExist:
            self.log_message("ERROR: There's no flight with such id!")
        # then change parameters, if needed
        today = datetime.datetime.strptime(departure_date, "%Y-%m-%d").date()
        nextmonth = today + relativedelta(days=7)
        self.PARSE_SETTINGS = {
            'originAirport': self.flight.origin,
            'destinationAirport': self.flight.destination,
            'travelMonth': str(today.month),
            'travelDay': str(today.day),
            'nextMonth': str(nextmonth.month),
            'nextMonthDay': str(nextmonth.day),
            'tripType': 'oneWay',
            'adultPassengerCount': '1',
            'childPassengerCount': '0',
            'flightNumber': self.flight.flight_number,
            'departureDate': today.strftime('%m/%d/%Y'),  # THIS IS REALLY IMPORTANT!!!!
        }


    def start_requests(self):
        for cabin in self.CABIN_CHOICES:
            try:

                yield FormRequest(
                    url=self.start_urls[0],
                    method='POST',
                    cookies=self.cookies,
                    formdata={
                        'flightNumber': self.PARSE_SETTINGS['flightNumber'],
                        'departureDate': self.PARSE_SETTINGS['departureDate'],
                        'originAirport': self.PARSE_SETTINGS['originAirport'],
                        'destinationAirport': self.PARSE_SETTINGS['destinationAirport'],
                        'cabin': cabin,
                        'currentCalForm': 'dep',
                        'returnUrl': 'popup',
                        'airportLookupRequired': 'true',
                    },
                    callback=getattr(self, 'callback_'+cabin),
                )
            except:
                self.log_message('ERROR: while parsing cabin  %s' % cabin)
                continue

    def callback_coach(self, response):
        return self._callback(response, 'coach')

    def callback_business(self, response):
        return self._callback(response, 'business')

    def callback_first(self, response):
        return self._callback(response, 'first')

    def _callback(self, response, cabin):
        """
        Main function that will parse all needed info for all of the cabins and save all seats to DB
        """
        # first off we'll save html-page
        self.save_html(response, cabin)
        try:
            flight = ParsedFlight.objects.filter(flight=self.flight, monthly=self.monthly).order_by('-when_created')[0]
        except IndexError:
            self.log_message("ERROR: There's no such flight #%s" % self.PARSE_SETTINGS['flightNumber'])
            return ''
        selector = Selector(response)
        self.parse_seats(flight, selector, cabin)

    def parse_legend(self, selector):
        """
        Takes a Selector object and fills self.seat_legend with data
        """
        import re
        stars = selector.xpath('//div[contains(@class,"legend-img")]/img[contains(@class,"mpp-sym")]/@src')
        extra_prices = selector.xpath('//span[contains(@class,"legend-price")]/text()')
        if len(stars) == len(extra_prices):
            # if images with stars count is equal to extra prices count moving forth
            clean_stars = map(lambda x: re.sub("[^0-9]", "", x), stars.extract())
            clean_extra_prices = map(lambda x: re.sub("[^0-9]", "", x), extra_prices.extract())
            self.seat_legend = dict(zip(clean_stars, clean_extra_prices))

    def parse_seats(self, flight, selector, cabin):
        # first off lets delete old seats
        flight.seat_set.filter(cabin=Seat.SEAT_CLASS_DICT.get(cabin, 0)).delete()
        if not self.seat_legend:
            # if the seat legend is empty we'll try to fill it with data
            self.parse_legend(selector)
        if self.seat_legend:
            # saving legend to db
            try:
                flight.one_star = self.seat_legend.get('1', 0)
                flight.two_stars = self.seat_legend.get('2', 0)
                flight.three_stars = self.seat_legend.get('3', 0)
                flight.four_stars = self.seat_legend.get('4', 0)
            except IndexError:
                self.log_message('ERROR: saving legend')
        #saving seats as html
        html = safe_list_get(selector.xpath('//div[@id="seatMapContainer"]').extract(), 0)
        setattr(flight, cabin+'_html', html)
        #saving seats to db as objects
        seat_list = selector.xpath('//div[contains(@class,"seat-wrapper")]')
        for seat in seat_list:
            self.parse_seat(seat, flight, cabin)
        flight.save()

    def parse_seat(self, seat, flight, cabin):
        available = False
        extra = 0
        name = safe_list_get(seat.xpath('.//img[contains(@class,"seat-img")]/@alt').extract(), 0) or 'EXIT'
        seat_cabin = Seat.SEAT_CLASS_DICT.get(cabin, 0)
        available_image_src = safe_list_get(seat.xpath('.//img[contains(@class,"seat-img")]/@src').extract(), 0)
        if available_image_src == u'/content/images/seatMap/seat-available.png':
            available = True
            import re
            extra_string = safe_list_get(seat.xpath('.//img[contains(@class,"seat-mpp-sym")]/@src').extract(), 0, '')
            extra = re.sub('[^0-9]', '', extra_string) or 0
        seat = Seat.objects.create(
            flight=flight,
            name=name,
            cabin=seat_cabin,
            extra=extra,
            available=available
        )
        seat.save()

    def save_html(self, response, cabin):
        pass
        # filename = response.url.split("/")[-2] + '_%s.html' % cabin
        # open(filename, 'wb').write(response.body)

