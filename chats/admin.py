from django.contrib import admin
from .models import Comment
from products.models import Product


class CommentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'msg', 'listing', 'send_time', 'active')
    list_filter = ('sender', 'send_time', 'active')
    search_fields = ('sender', 'msg')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Comment, CommentAdmin)