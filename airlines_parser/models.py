import json
from django.db import models
from django.utils.text import slugify
from helper.models_base import TimeItem


class Airline(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        db_table = 'airlines_parser_airline'

    def __unicode__(self):
        return self.name

class Flight(TimeItem):
    airline = models.ForeignKey(Airline, blank=False, null=False)
    flight_number = models.CharField(max_length=20, blank=False, null=False)
    origin = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        db_table = 'airlines_parser_flight'

    def __unicode__(self):
        return 'Flight #%s from %s to %s by %s.' % (self.flight_number, self.origin, self.destination, self.airline)

    @property
    def last_parse_date(self):
        try:
            return self.parsedflight_set.all().order_by('-when_created')[0].when_created
        except:
            return '-----'


class ParsedFlight(TimeItem):
    flight = models.ForeignKey(Flight, blank=False, null=True)
    monthly = models.IntegerField(max_length=1, blank=True, default=0)
    departure_date = models.CharField(max_length=50, blank=True, null=True)
    departure = models.CharField(max_length=50, blank=True, null=True)
    arrival = models.CharField(max_length=50, blank=True, null=True)
    prices = models.TextField(max_length=50, blank=True, null=True, default="")
    one_star = models.CharField(max_length=50, blank=True, null=True)  # additional price for one star
    two_stars = models.CharField(max_length=50, blank=True, null=True)  # additional price for two stars
    three_stars = models.CharField(max_length=50, blank=True, null=True)  # additional price for main cabin
    four_stars = models.CharField(max_length=50, blank=True, null=True)  # additional price for main cabin
    coach_html = models.TextField(blank=True, null=True)  # html
    business_html = models.TextField(blank=True, null=True)  # html
    first_html = models.TextField(blank=True, null=True)  # html

    class Meta:
        db_table = 'airlines_parser_parsed_flight'

    def _get_cabin_count(self, cabin):
        return Seat.objects.filter(flight=self, available=True, cabin=cabin).count()

    @property
    def get_coach_count(self):
        return self._get_cabin_count(1)

    @property
    def get_business_count(self):
        return self._get_cabin_count(2)

    @property
    def get_first_count(self):
        return self._get_cabin_count(3)

    def parse_prices(self, array, millisecond_time):
        try:
            for fare, price in json.loads(self.prices).items():
                if slugify(fare) in array:
                    array[slugify(fare)]['array'].append((millisecond_time, int(float(price))))
                else:
                    array[slugify(fare)] = {'array': [(millisecond_time, int(float(price)))]}
        except TypeError:
            print "Type Error in parse_price"


class Seat(models.Model):
    # is there extra pay for the seat
    SEAT_EXTRA = (
        (0, 'None'),
        (1, 'One Star'),
        (2, 'Two Stars'),
        (3, 'Three Stars'),
        (3, 'Four Stars'),
    )
    # class of the seat
    SEAT_CLASS = (
        (0, 'None'),
        (1, 'coach'),
        (2, 'business'),
        (3, 'first'),
    )
    SEAT_CLASS_DICT = {
        'coach': 1,
        'business': 2,
        'first': 3,
    }
    flight = models.ForeignKey(ParsedFlight, blank=False)
    name = models.CharField(max_length=10, blank=False)  # 16A
    available = models.BooleanField(blank=True, default=False)
    extra = models.PositiveIntegerField(max_length=1, blank=True, default=0, choices=SEAT_EXTRA)
    cabin = models.PositiveIntegerField(max_length=1, blank=True, default=0, choices=SEAT_CLASS)

    class Meta:
        db_table = 'airlines_parser_seat'


class Cookie(TimeItem):
    cookie_keys = models.TextField(blank=False, default='', null=True)

    class Meta:
        db_table = 'airlines_parser_cookie'