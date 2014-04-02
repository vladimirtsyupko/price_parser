# -*- coding: utf-8 -*-
import subprocess
import datetime

__author__ = 'vladimir'


def parse_flight_from_command_line(flight_id=666,
                                   departure_date=datetime.date.today(),
                                   monthly=0):
    # scrapy crawl myspider -a originAirport='JFK' -a destinationAirport='SYD' -a departureDate='2014-03-18' -a flightNumber='3' -a domain=system
    args = locals()
    COMMANDS = {
        0: ['scrapy', 'crawl', 'parse_cookies'],
        1: ['scrapy', 'crawl', 'parse_price'],
        2: ['scrapy', 'crawl', 'parse_available_seats'],
    }
    for name, field in args.items():
        COMMANDS[1].append('-a')
        COMMANDS[1].append('%s=%s' % (name, field))
        COMMANDS[2].append('-a')
        COMMANDS[2].append('%s=%s' % (name, field))
    for k, command in COMMANDS.items():
        # print k, command
        test = subprocess.call(command)