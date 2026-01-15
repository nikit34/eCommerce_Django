from django.urls import path, re_path

from .views import (
    cart_home, cart_update,
    checkout_home,
    checkout_done_view
)


urlpatterns = [
    path('', cart_home, name='home'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update'),
    re_path(r'^checkout/success/(?P<orderID>[\w\-]+)/$', checkout_done_view, name='success'),
]
