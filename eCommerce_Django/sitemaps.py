from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from django.views.generic import TemplateView

from products.models import Product
from orders.models import Order
from addresses.models import Address


class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            'about',
            'contact',
            'login',
            'logout',
            'register',
            'collection',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()


class OrderSitemap(Sitemap):
    def items(self):
        return Order.objects.all()


class AddressesSitemap(Sitemap):
    def items(self):
        return Address.objects.all()


global_maps = {
    'products': ProductSitemap,
    'orders': OrderSitemap,
    'addresses': AddressesSitemap,
    'static': StaticViewSitemap
}


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'