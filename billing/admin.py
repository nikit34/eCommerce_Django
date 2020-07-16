from django.contrib import admin
from .models import BillingProfile, Card, PaypalCard, Charge, PaypalCharge


admin.site.register(BillingProfile)

admin.site.register(Card)

admin.site.register(PaypalCard)

admin.site.register(Charge)

admin.site.register(PaypalCharge)
