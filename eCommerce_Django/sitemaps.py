from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from django.views.generic import TemplateView

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


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'