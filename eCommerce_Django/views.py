from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.utils.translation import gettext
from django.views.decorators.csrf import csrf_exempt
import git

from carts.models import Cart
from products.models import Product

from .forms import ContactForm


class ProductListView(ListView):
    template_name = 'home_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        if request.GET.get("price") == "descend":
            return Product.objects.order_by('price')
        elif request.GET.get("price") == "ascend":
            return Product.objects.order_by('-price')
        elif request.GET.get("time_update") == "descend":
            return Product.objects.order_by('timestamp')
        elif request.GET.get("time_update") == "ascend":
            return Product.objects.order_by('-timestamp')
        else:
            return Product.objects.all()


def about_page(request):
    context = {
        "title": gettext("About"),
        "content": gettext("Welcome to about page!")
    }
    return render(request, "contact/about.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    support_email = getattr(settings, 'SUPPORT_EMAIL', None)
    context = {
        "title": gettext("Contact"),
        "content": gettext("Here you can leave your feedback."),
        "form": contact_form,
    }
    if contact_form.is_valid():
        fullname = contact_form.cleaned_data['fullname']
        email = contact_form.cleaned_data['email']
        content = contact_form.cleaned_data['content']
        msg_content = gettext('Send with contact email: ') + email + '\n\n' + content
        try:
            send_mail(fullname, msg_content, email, [support_email])
        except BadHeaderError:
            return HttpResponse(gettext('Invalid header found.'))
        if request.is_ajax():
            return JsonResponse({'message': gettext('Thank you for your submission')})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return JsonResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        repo = git.Repo('/home/OlyaStudio/olyastudio.pythonanywhere.com/.git/')
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse(gettext("Update code on server"))
    else:
        return HttpResponse(gettext("ERROR: Could`t update the code on server"))
