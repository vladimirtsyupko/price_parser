# -*- coding: utf-8 -*-
from django.db import models
from helper.models_base import TimeItem


class Shop(models.Model):
    title = models.CharField(blank=False, max_length=30, null=True)
    url = models.CharField(blank=False, max_length=30, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'price_parser_shop'


class Product(TimeItem):
    name = models.TextField(blank=False, max_length=300, null=True)
    active = models.BooleanField(blank=True, default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'price_parser_product'


class ProductSku(models.Model):
    shop = models.ForeignKey(Shop, blank=False)
    product = models.ForeignKey(Product, blank=False)
    sku = models.CharField(blank=False, max_length=30, null=True)

    def __unicode__(self):
        return "%s %s %s" % (self.sku, self.product, self.shop)

    class Meta:
        db_table = 'price_parser_product_sku'


class ParsedProductPrice(TimeItem):
    shop = models.ForeignKey(Shop, blank=False)
    product = models.ForeignKey(Product, blank=False)
    price = models.DecimalField(blank=True, max_digits=7, decimal_places=2, null=True)
    price_usd = models.DecimalField(blank=True, max_digits=7, decimal_places=2, null=True)
    currency = models.CharField(blank=True, max_length=30, null=True)
    source = models.CharField(blank=True, max_length=30, null=True)
    in_stock = models.BooleanField(blank=True,)
    image = models.URLField(blank=True, max_length=200, null=True)
    url = models.URLField("product url", blank=True, max_length=200)
    heading = models.CharField("product description", blank=True, max_length=500)

    class Meta:
        db_table = 'price_parser_product_price'
