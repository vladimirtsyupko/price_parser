# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from .models import Flight, ParsedFlight, Airline


class FlightAdmin(admin.ModelAdmin):
    pass


class ParsedFlightAdmin(admin.ModelAdmin):
    pass


class AirlineAdmin(admin.ModelAdmin):
    pass


admin.site.register(Flight, FlightAdmin)
admin.site.register(ParsedFlight, ParsedFlightAdmin)
admin.site.register(Airline, AirlineAdmin)