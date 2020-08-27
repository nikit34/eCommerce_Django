from django.contrib import admin

from .models import Product, ProductFile


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'delivery']
    inlines = [ ProductFileInline ]

    class Meta:
        model = Product

    class Media:
        js = ('/static/js/tinyInject.js',)


admin.site.register(Product, ProductAdmin)
