from django.test import TestCase
from django import forms

from accounts.forms import (
    LoginForm, RegisterForm,
    UserAdminCreationForm, UserDetailChangeForm
)
from accounts.views import LoginView
from accounts.models import User


class LoginFormTest(TestCase):
    def test_email_label(self):
        request = LoginView.as_view()
        form = LoginForm(request=request)
        self.assertEqual(form.fields['email'].label, 'Email')

    def test_password_label(self):
        request = LoginView.as_view()
        form = LoginForm(request)
        self.assertEqual(form.fields['password'].label, 'Password')


class RegisterFormTest(TestCase):
    def test_password_label(self):
        form = RegisterForm()
        self.assertTrue(
            form.fields['password1'].label == 'Password' and
            form.fields['password2'].label == 'Password confirmation'
        )


class UserAdminCreationFormTest(TestCase):
    def test_password_label(self):
        form = RegisterForm()
        self.assertTrue(
            form.fields['password1'].label == 'Password' and
            form.fields['password2'].label == 'Password confirmation'
        )


class UserDetailChangeFormTest(TestCase):
    def test_full_name_label(self):
        form = UserDetailChangeForm()
        self.assertEqual(form.fields['full_name'].label, 'Name')