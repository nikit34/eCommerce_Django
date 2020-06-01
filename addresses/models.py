from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping' , 'Shipping'),
    ('','')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, default='Russia')
    state= models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return '{line1},\n{line2}\n{city},\n{state}, {postal},\n{country}'.format(
            line1 = self.address_line_1,
            line2 = self.address_line_2 or '',
            city = self.city,
            state = self.state,
            postal = self.postal_code,
            country = self.country,
        )
