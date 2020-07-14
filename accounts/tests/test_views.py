from django.test import TestCase
from django.urls import reverse

from accounts.models import User, EmailActivation, GuestEmail
from accounts.forms import GuestForm
from accounts.views import GuestRegisterView


class AccountHomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def test_url_get(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)


class GuestRegisterViewTest(TestCase):
    def test_url_get(self):
        response = self.client.get('/en/register/')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get('/en/register/')
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_form_invalid(self):
        response = self.client.get('/en/register/')
        form = GuestForm(response)
        guest_register_view = GuestRegisterView()
        invalid = guest_register_view.form_invalid(form)
        self.assertEqual(invalid.status_code, 302)
