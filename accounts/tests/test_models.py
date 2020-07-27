from django.test import TestCase
from django.core import mail

from accounts.models import User, EmailActivation, GuestEmail


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_full_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'full name')

    def test_email_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 255)

    def test_full_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('full_name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_email(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.email}'
        self.assertEqual(expected_object_name, str(user))

    def test_get_full_name(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_full_name(), 'Test')

    def test_get_short_name(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_short_name(), 'usermodeltest@gmail.com')


class GuestEmailModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GuestEmail.objects.create(email='guestemailmodeltest@gmail.com')

    def test_email_label(self):
        guest_email = GuestEmail.objects.get(id=1)
        field_label = guest_email._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_object_name_is_email(self):
        guest_email = GuestEmail.objects.get(id=1)
        expected_object_name = f'{guest_email.email}'
        self.assertEqual(expected_object_name, str(guest_email))


class EmailActivationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            email='usermodeltest@gmail.com',
            full_name='Test',
            password='test'
        )
        EmailActivation.objects.create(
            user=user,
            email='emailactivationmodeltest@gmail.com'
        )

    def test_user_label(self):
        email_activation = EmailActivation.objects.get(id=1)
        field_label = email_activation._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_email_label(self):
        email_activation = EmailActivation.objects.get(id=1)
        field_label = email_activation._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_object_name_is_email(self):
        email_activation = EmailActivation.objects.get(id=1)
        expected_object_name = f'{email_activation.email}'
        self.assertEqual(expected_object_name, str(email_activation))

    def test_activate(self):
        email_activation = EmailActivation.objects.get(id=1)
        self.assertTrue(email_activation.activate())

    def test_regenerate(self):
        email_activation = EmailActivation.objects.get(id=1)
        self.assertTrue(email_activation.regenerate())

    def test_send_activation(self):
        email_activation = EmailActivation.objects.get(id=1)
        self.assertEqual(email_activation.send_activation(), 1)
