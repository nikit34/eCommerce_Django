import os
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from wsgiref.util import FileWrapper
from mimetypes import guess_type
from django.conf import settings
from django.core import serializers

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from chats.models import Comment
from chats.forms import CommentForm
from .models import Product, ProductFile


class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False)
        return views


class ProductListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def post(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        new_comment = None
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.listing = self.object
            new_comment.sender = request.user
            new_comment.save()
            context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
            return self.render_to_response(context=context)
        return JsonResponse({'error': 'Form is not valid'}, status=400)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        slug = self.kwargs.get('slug')
        slides = ProductFile.objects.all().filter(product__slug=slug)
        context['slides'] = slides
        context['comments'] = ''
        context['comment_form'] = CommentForm()
        try:
            instance = Product.objects.get(slug=slug, active=True)
            context['comments'] = instance.comments.filter(active=True)
            instance.views = instance.views + 1
            context['views'] = instance.views
            instance.save()
        except Comment.DoesNotExist:
            raise Http404('Not found..')
        except:
            raise Http404('Indefinite')
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not found..')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('Indefinite')
        return instance


class ProductFeaturedListView(ListView):
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name = 'products/featured-detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        file_root = settings.PROTECTED_ROOT
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        filepath = download_obj.file.path
        final_filepath = os.path.join(file_root, filepath)
        with open(final_filepath, 'rb') as f:
            wrapper = FileWrapper(f)
            mimetype = 'application/force-download'
            gussed_mimetype = guess_type(filepath)[0]
            if gussed_mimetype:
                mimetype = gussed_mimetype
            response = HttpResponse(wrapper, content_type=mimetype)
            response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
            response["X-SendFile"] = str(download_obj.name)
            return response
        return redirect(download_obj.get_default_url())