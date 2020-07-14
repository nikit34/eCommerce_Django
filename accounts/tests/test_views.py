from django.test import TestCase

from accounts.models import User, EmailActivation, GuestEmail


class GuestRegisterView(TestCase):
    @classmethod
    def setUpTestData(cls):
        GuestEmail.objects.create(email='guestemailmodeltest@gmail.com')

    def test_url_get(self):
        response = self.client.get('/en/register/')
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get('/en/register/')
        self.assertTemplateUsed(response, 'accounts/register.html')
