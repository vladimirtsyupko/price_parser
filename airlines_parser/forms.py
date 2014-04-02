# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.admin import widgets


class FlightParseForm(forms.Form):
    origin_airport = forms.CharField(max_length=10, required=True)
    destination_airport = forms.CharField(max_length=10, required=True)
    flight_number = forms.CharField(max_length=10, required=True)
    departure_date = forms.DateField(initial=datetime.date.today, required=True,  widget = widgets.AdminDateWidget)