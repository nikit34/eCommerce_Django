from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from carts.models import Cart
from products.models import Product

from .forms import ContactForm


class ProductListView(ListView):
    template_name = 'home_page.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

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
        "title": "About",
        "content": "Welcome to about page!"
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "Welcome to contact page!",
        "form": contact_form,
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({'message': 'Thank you for your submission'})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return JsonResponse(errors, status=400, content_type='application/json')

    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get("fullname"))
    #     print(request.POST.get("email"))
    #     print(request.POST.get("content"))
    return render(request, "contact/view.html", context)
