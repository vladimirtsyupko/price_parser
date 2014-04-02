# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Airline'
        db.create_table('airlines_parser_airline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'airlines_parser', ['Airline'])

        # Adding model 'Flight'
        db.create_table('airlines_parser_flight', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('when_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('airline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['airlines_parser.Airline'])),
            ('flight_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('destination', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'airlines_parser', ['Flight'])

        # Adding model 'ParsedFlight'
        db.create_table('airlines_parser_parsed_flight', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('when_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['airlines_parser.Flight'], null=True)),
            ('monthly', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1, blank=True)),
            ('departure_date', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('departure', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('arrival', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('prices', self.gf('django.db.models.fields.TextField')(default='', max_length=50, null=True, blank=True)),
            ('one_star', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('two_stars', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('three_stars', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('four_stars', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('coach_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('business_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('first_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'airlines_parser', ['ParsedFlight'])

        # Adding model 'Seat'
        db.create_table('airlines_parser_seat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['airlines_parser.ParsedFlight'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extra', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=1, blank=True)),
            ('cabin', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=1, blank=True)),
        ))
        db.send_create_signal(u'airlines_parser', ['Seat'])

        # Adding model 'Cookie'
        db.create_table('airlines_parser_cookie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('when_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('cookie_keys', self.gf('django.db.models.fields.TextField')(default='', null=True)),
        ))
        db.send_create_signal(u'airlines_parser', ['Cookie'])


    def backwards(self, orm):
        # Deleting model 'Airline'
        db.delete_table('airlines_parser_airline')

        # Deleting model 'Flight'
        db.delete_table('airlines_parser_flight')

        # Deleting model 'ParsedFlight'
        db.delete_table('airlines_parser_parsed_flight')

        # Deleting model 'Seat'
        db.delete_table('airlines_parser_seat')

        # Deleting model 'Cookie'
        db.delete_table('airlines_parser_cookie')


    models = {
        u'airlines_parser.airline': {
            'Meta': {'object_name': 'Airline'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'airlines_parser.cookie': {
            'Meta': {'object_name': 'Cookie'},
            'cookie_keys': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'airlines_parser.flight': {
            'Meta': {'object_name': 'Flight'},
            'airline': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['airlines_parser.Airline']"}),
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'flight_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'airlines_parser.parsedflight': {
            'Meta': {'object_name': 'ParsedFlight', 'db_table': "'airlines_parser_parsed_flight'"},
            'arrival': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'business_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'coach_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'departure': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'departure_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'first_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['airlines_parser.Flight']", 'null': 'True'}),
            'four_stars': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1', 'blank': 'True'}),
            'one_star': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prices': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'three_stars': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'two_stars': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'airlines_parser.seat': {
            'Meta': {'object_name': 'Seat'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cabin': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1', 'blank': 'True'}),
            'extra': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1', 'blank': 'True'}),
            'flight': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['airlines_parser.ParsedFlight']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['airlines_parser']