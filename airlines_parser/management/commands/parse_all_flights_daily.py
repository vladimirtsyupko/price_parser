#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from airlines_parser.models import Flight
from helper.functions import parse_flight_from_command_line
from django.core.management.base import BaseCommand, CommandError
from airlines_parser import settings


class Command(BaseCommand):
    """
    Example ./manage.py parse_flight_daily
    """
    # args = '<flight_id ...>'
    help = 'Run this command and all existing flights will be parsed'

    def handle(self, *args, **options):
        with open(settings.BASE_DIR+"log.txt", "a") as myfile:
            myfile.write('[%s]:[%s]\n' % (datetime.datetime.now(), 'Cron daily flight run'))
        flights = Flight.objects.all()
        for flight in flights:
            try:

                parse_flight_from_command_line(
                    flight_id=flight.id,
                    departure_date=datetime.date.today(),
                    monthly=0)
            except Flight.DoesNotExist:
                raise CommandError('There is an error occurred with flight number="%s"' % flight.id)