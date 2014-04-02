#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from airlines_parser.models import Flight
from helper.functions import parse_flight_from_command_line
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Example ./manage.py parse_flight_month 1
    """
    args = '<flight_id ...>'
    help = 'Parse flight for a month from current date'

    def handle(self, *args, **options):

        flights = Flight.objects.all()
        for flight in flights:
            for days in range(0, 31):
                parse_flight_from_command_line(
                    flight_id=flight.id,
                    departure_date=datetime.date.today() + datetime.timedelta(days=days),
                    monthly=1)
            # raise CommandError('There is no flight with number="%s"' % arg)