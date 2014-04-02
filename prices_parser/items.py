from scrapy.contrib.djangoitem import DjangoItem
from scrapy.item import Item, Field



class PricesItem(Item):
    heading = Field()
    title = Field()
    price = Field()
    price_usd = Field()
    curr = Field()
    url = Field()
    pid = Field()
    date = Field()
    tmstamp = Field()
    source = Field()
    sku = Field()
    in_stock = Field()
    image = Field()
    image_paths = Field()


class ParsedPriceItem(Item):
    shop_id = Field()
    product_id = Field()
    heading = Field()
    title = Field()
    price = Field()
    price_usd = Field()
    currency = Field()
    url = Field()
    when_created = Field()
    source = Field()
    # sku = Field()
    in_stock = Field()
    image = Field()


    # image_paths = Field()