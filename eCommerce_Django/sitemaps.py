from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from products.models import Product


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()



global_maps = {
    'products': ProductSitemap,
    'static': StaticViewSitemap
}