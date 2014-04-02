# -*- coding: utf-8 -*-
import json
from pprint import pprint
import subprocess
import datetime
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
import time
from django.utils.text import slugify
from airlines_parser.forms import FlightParseForm
from airlines_parser.models import ParsedFlight, Flight


def index(request):
    return render(request, 'main.html')


@login_required
def flight_list(request):

    flights = Flight.objects.all()
    return render(request, 'index.html', {'flights': flights})


@login_required
def flight_detail(request):
    flights = get_list_or_404(ParsedFlight)

    return render(request, 'flight_detail.html', {'flights': flights})


@login_required
def get_flight_info(request):
    flight_id = request.GET.get('flight_number', 0)
    flight = get_object_or_404(Flight, pk=flight_id)
    today_prices = {}
    month_ago_prices = {}
    today_seats = {
        'coach': {
            'array': []
        },
        'business': {
            'array': []
        },
        'first': {
            'array': []
        },
    }
    month_ago_seats = {
        'coach': {
            'array': []
        },
        'business': {
            'array': []
        },
        'first': {
            'array': []
        },
    }
    dates = {}
    flight_info = {}
    try:
        flight_info = dict(flight.__dict__.items() + flight.parsedflight_set.all().order_by('-when_created')[0].__dict__.items())
    except IndexError:
        print 'errorororoor'
    for flight in flight.parsedflight_set.filter():
        departure_date = datetime.datetime.strptime(flight.departure_date, "%Y-%m-%d")
        millisecond_time = int(round(time.mktime(departure_date.timetuple()))*1000)
        if flight.monthly == 1:
            clear_month = departure_date.strftime("%m")  # b
            if departure_date.year not in dates:
                dates[departure_date.year] = {}
            if clear_month not in dates[departure_date.year]:
                dates[departure_date.year][clear_month] = {}
            dates[departure_date.year][clear_month][departure_date.day] = flight.departure_date

            flight.parse_prices(month_ago_prices, millisecond_time)
            month_ago_seats['coach']['array'].append((millisecond_time, flight.get_coach_count))
            month_ago_seats['business']['array'].append((millisecond_time, flight.get_business_count))
            month_ago_seats['first']['array'].append((millisecond_time, flight.get_first_count))
        else:
            flight.parse_prices(today_prices, millisecond_time)
            today_seats['coach']['array'].append((millisecond_time, flight.get_coach_count))
            today_seats['business']['array'].append((millisecond_time, flight.get_business_count))
            today_seats['first']['array'].append((millisecond_time, flight.get_first_count))
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    return HttpResponse(json.dumps({'dates': dates,
                                    'today_prices': today_prices,
                                    'month_ago_prices': month_ago_prices,
                                    'today_seats': today_seats,
                                    'month_ago_seats': month_ago_seats,
                                    'flight_info': flight_info}, default=dthandler), 'json')


@login_required
def get_flight_info_by_date(request):
    flight_id = request.GET.get('flight_number', 0)
    date = request.GET.get('date', 0)
    flight = get_object_or_404(Flight, pk=flight_id)
    today_prices = {}
    month_ago_prices = {}
    today_seats = {
        'coach': {
            'array': []
        },
        'business': {
            'array': []
        },
        'first': {
            'array': []
        },
    }
    month_ago_seats = {
        'coach': {
            'array': []
        },
        'business': {
            'array': []
        },
        'first': {
            'array': []
        },
    }
    today_info = {}
    month_ago_info = {}
    try:
        print datetime.date.today()
        parsed_today = ParsedFlight.objects.get(monthly=0,
                                                departure_date=date,
                                                flight=flight)
        millisecond_time = int(round(time.mktime(datetime.datetime.strptime(parsed_today.departure_date, "%Y-%m-%d").timetuple()))*1000)
        parsed_today.parse_prices(today_prices, millisecond_time)
        today_seats['coach']['array'].append((millisecond_time, parsed_today.get_coach_count))
        today_seats['business']['array'].append((millisecond_time, parsed_today.get_business_count))
        today_seats['first']['array'].append((millisecond_time, parsed_today.get_first_count))
        today_info = parsed_today.__dict__
    except ParsedFlight.DoesNotExist:
        print(json.dumps('not enough info some of the pared flights are missing'))

    try:
        parsed_month_ago = ParsedFlight.objects.filter(monthly=1,
                                                       departure_date=date,
                                                       flight=flight).order_by('-when_created')[0]
        millisecond_time = int(round(time.mktime(datetime.datetime.strptime(parsed_month_ago.departure_date, "%Y-%m-%d").timetuple()))*1000)
        parsed_month_ago.parse_prices(month_ago_prices, millisecond_time)
        month_ago_seats['coach']['array'].append((millisecond_time, parsed_month_ago.get_coach_count))
        month_ago_seats['business']['array'].append((millisecond_time, parsed_month_ago.get_business_count))
        month_ago_seats['first']['array'].append((millisecond_time, parsed_month_ago.get_first_count))

        month_ago_info = parsed_month_ago.__dict__
    except ParsedFlight.DoesNotExist:
        print(json.dumps('not enough info some of the pared flights are missing'))
    flight_info = flight.__dict__


    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    return HttpResponse(json.dumps({'today_prices': today_prices,
                                    'month_ago_prices': month_ago_prices,
                                    'today_seats': today_seats,
                                    'month_ago_seats': month_ago_seats,
                                    'flight_info': flight_info,
                                    'today_info': today_info,
                                    'month_ago_info': month_ago_info},
                                   default=dthandler), 'json')

@login_required
def parse_flight(request):
    # scrapy crawl myspider -a origin_airport='JFK' -a destination_airport='SYD' -a departure_date='2014-03-18' -a flight_number='3'
    if request.method == "POST":
        form = FlightParseForm(request.POST)
        if form.is_valid():
            COMMANDS = {
                0: ['scrapy', 'crawl', 'parse_cookies'],
                1: ['scrapy', 'crawl', 'parse_price'],
                2: ['scrapy', 'crawl', 'parse_available_seats'],
            }
            for field in form.cleaned_data:
                COMMANDS[1].append('-a')
                COMMANDS[1].append('%s=%s' % (field, form.data[field]))
                COMMANDS[2].append('-a')
                COMMANDS[2].append('%s=%s' % (field, form.data[field]))
            for k, command in COMMANDS.items():
                test = subprocess.call(command)
    else:
        form = FlightParseForm()
    return render(request, 'parse_form.html', {'form': form})
