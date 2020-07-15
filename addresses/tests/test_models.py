from django.test import TestCase

from addresses.models import Address
from billing.models import BillingProfile
from accounts.models import User


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        billing_profile = BillingProfile.objects.create(
            email='billingprofilemodeltest@gmail.com'
        )
        Address.objects.create(
            billing_profile=billing_profile,
            address_type='billing',
            address_line_1='Testogorsk',
            state='Testovskya',
            city='Testovo',
            postal_code='87654321'
        )

    def test_billing_profile_label(self):
        address = Address.objects.get(id=1)
        field_label = address._meta.get_field('billing_profile').verbose_name
        self.assertEqual(field_label, 'billing profile')

    def test_object_name_is_email(self):
        address = Address.objects.get(id=1)
        expected_object_name = f'{address.address_line_1}'
        self.assertEqual(expected_object_name, str(address))

    def test_get_short_address(self):
        address = Address.objects.get(id=1)
        self.assertEqual(address.get_short_address(), ' Testogorsk, Testovo')

    def test_get_address(self):
        address = Address.objects.get(id=1)
        self.assertEqual(address.get_address(), '\nTestogorsk,\n\nTestovo,\nTestovskya, 87654321,\nRussia')
