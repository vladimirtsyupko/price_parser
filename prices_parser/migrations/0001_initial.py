# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shop'
        db.create_table('price_parser_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal(u'prices_parser', ['Shop'])

        # Adding model 'Product'
        db.create_table('price_parser_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('when_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=300, null=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'prices_parser', ['Product'])

        # Adding model 'ProductSku'
        db.create_table('price_parser_product_sku', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices_parser.Shop'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices_parser.Product'])),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal(u'prices_parser', ['ProductSku'])

        # Adding model 'ParsedProductPrice'
        db.create_table('price_parser_product_price', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('when_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices_parser.Shop'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prices_parser.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('price_usd', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('in_stock', self.gf('django.db.models.fields.BooleanField')()),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal(u'prices_parser', ['ParsedProductPrice'])


    def backwards(self, orm):
        # Deleting model 'Shop'
        db.delete_table('price_parser_shop')

        # Deleting model 'Product'
        db.delete_table('price_parser_product')

        # Deleting model 'ProductSku'
        db.delete_table('price_parser_product_sku')

        # Deleting model 'ParsedProductPrice'
        db.delete_table('price_parser_product_price')


    models = {
        u'prices_parser.parsedproductprice': {
            'Meta': {'object_name': 'ParsedProductPrice', 'db_table': "'price_parser_product_price'"},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'in_stock': ('django.db.models.fields.BooleanField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'price_usd': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices_parser.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices_parser.Shop']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'prices_parser.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'price_parser_product'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True'}),
            'when_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'when_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'prices_parser.productsku': {
            'Meta': {'object_name': 'ProductSku', 'db_table': "'price_parser_product_sku'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices_parser.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prices_parser.Shop']"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        u'prices_parser.shop': {
            'Meta': {'object_name': 'Shop', 'db_table': "'price_parser_shop'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        }
    }

    complete_apps = ['prices_parser']