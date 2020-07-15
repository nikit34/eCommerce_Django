from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from addresses.models import Address
from billing.models import BillingProfile
from addresses.views import AddressListView


class AddressListViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/addresses/')
        self.assertRedirects(response, '/login/?next=/en/addresses/', fetch_redirect_response=False)

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/addresses/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('addresses'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/addresses/')
        self.assertTemplateUsed(response, 'addresses/list.html')

    def test_correct_context(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/addresses/')
        self.assertEqual(str(response.context['user']), 'usermodeltest@gmail.com')


class AddressUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        billing_profile = BillingProfile.objects.create(
            email='billingprofilemodeltest@gmail.com'
        )
        billing_profile.save()
        self.address = Address.objects.create(
            billing_profile=billing_profile,
            address_type='billing',
            address_line_1='Testogorsk',
            state='Testovskya',
            city='Testovo',
            postal_code='87654321'
        )

    def test_url_get_not_logged_in(self):
        response = self.client.get(f"/en/addresses/{self.address.pk}/")
        self.assertRedirects(response, f"/login/?next=/en/addresses/{self.address.pk}/", fetch_redirect_response=False)

    def test_address_pk(self):
        self.assertEqual(self.address.pk, 1)


class AddressCreateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        test_user.save()

    def test_url_get_not_logged_in(self):
        response = self.client.get('/en/addresses/create/')
        self.assertRedirects(response, '/login/?next=/en/addresses/create/', fetch_redirect_response=False)

    def test_url_get(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/addresses/create/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get(reverse('address-create'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/addresses/create/')
        self.assertTemplateUsed(response, 'addresses/update.html')

    def test_correct_context(self):
        login = self.client.login(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        response = self.client.get('/en/addresses/create/')
        self.assertEqual(str(response.context['user']), 'usermodeltest@gmail.com')
