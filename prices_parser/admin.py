from django.contrib import admin
from .models import Shop, Product, ParsedProductPrice, ProductSku


class ShopAdmin(admin.ModelAdmin):
    pass


class SkuLine(admin.TabularInline):
    extra = 3
    model = ProductSku


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        SkuLine,
    ]


class ProductSkuAdmin(admin.ModelAdmin):
    pass

class ParsedProductPriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductSku, ProductSkuAdmin)
admin.site.register(ParsedProductPrice, ParsedProductPriceAdmin)
