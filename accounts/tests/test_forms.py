from django.test import TestCase

from accounts.forms import LoginForm, RegisterForm, GuestForm
from accounts.views import LoginView

class LoginFormTest(TestCase):
    def test_email_label(self):
        request = LoginView.as_view()
        form = LoginForm(request=request)
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email')
        
