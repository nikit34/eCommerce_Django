from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView

from addresses.views import (
    AddressCreateView,
    AddressListView,
    AddressUpdateView,
    checkout_address_create_view,
    checkout_address_reuse_view
  )
from analytics.views import SalesView, SalesAjaxView
from accounts.views import LoginView, RegisterView
from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import LibraryView
from .views import ProductListView, about_page, contact_page


urlpatterns = [
  url(r'^$', ProductListView.as_view(), name='home'),
  url(r'^about/$', about_page, name='about'),
  url(r'^accounts/$', RedirectView.as_view(url='/account')),
  url(r'^account/', include("accounts.urls", namespace='account')),
  url(r'^accounts/', include("accounts.passwords.urls")),
  url(r'^address/$', RedirectView.as_view(url='/addresses')),
  url(r'^addresses/$', AddressListView.as_view(), name='addresses'),
  url(r'^addresses/create/$', AddressCreateView.as_view(), name='address-create'),
  url(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'),
  url(r'^analytics/sales/$', SalesView.as_view(), name='sales-analytics'),
  url(r'^analytics/sales/data/$', SalesAjaxView.as_view(), name='sales-analytics-data'),
  url(r'^contact/$', contact_page, name='contact'),
  url(r'^login/$', LoginView.as_view(), name='login'),
  url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
  url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
  url(r'^logout/$', LogoutView.as_view(), name='logout'),
  url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
  url(r'^cart/', include(('carts.urls','eCommerce_Django'), namespace='cart')),
  url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
  url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
  url(r'^register/$', RegisterView.as_view(), name='register'),
  url(r'^library/$', LibraryView.as_view(), name='library'),
  url(r'^orders/', include("orders.urls", namespace='orders')),
  url(r'^products/', include(('products.urls', 'eCommerce_Django'), namespace='products')),
  url(r'^search/', include(('search.urls', 'eCommerce_Django'), namespace='search')),
  url(r'^settings/$', RedirectView.as_view(url='/setting')),
  url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
  url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
  url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
