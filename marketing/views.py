from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView, View
from django.shortcuts import render, redirect
from django.utils.translation import gettext

from .forms import MarketingPreferenceForm
from .mixins import CsrfExemptMixin
from .models import MarketingPreference
from .utils import Mailchimp
from accounts.models import User

MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)
MAILCHIMP_EMAIL_ADMIN = getattr(settings, "MAILCHIMP_EMAIL_ADMIN", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'subscribe_form.html'
    success_url = '/webhooks/mailchimp/'
    success_message = gettext('Your email preferences have been updated. Thank you.')

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = gettext('Update Email Preferences')
        context['success_url'] = self.success_url
        context['email'] = self.request.user
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


class MailchimpWebhookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data = Mailchimp()
        list_id = data.list_id
        if str(list_id) == MAILCHIMP_EMAIL_LIST_ID:
            email = self.request.user.email
            qs = MarketingPreference.objects.filter(user__email__iexact=email)
            if qs.exists():
                response_status, response = data.check_substription_status(email)
                sub_status = response['status']
                is_subbed = None
                mailchimp_subbed = None
                if sub_status == "subscribed":
                    is_subbed, mailchimp_subbed = (False, False)
                    sub_status = "unsubscribed"
                elif sub_status == "unsubscribed":
                    is_subbed, mailchimp_subbed = (True, True)
                    sub_status = "subscribed"
                if is_subbed is not None and mailchimp_subbed is not None:
                    qs = MarketingPreference.objects.filter(user__email__iexact=email)
                    data.change_substription_status(email, sub_status)
                    qs.update(
                        subscribed=is_subbed,
                        mailchimp_subscribed=mailchimp_subbed,
                        mailchimp_msg=str(data)
                    )
            else:
                data.add_email(email)
                user = self.request.user
                obj, created = MarketingPreference.objects.get_or_create(user=user)
        return redirect('home')
