from django.db import models
from accounts.models import User
from products.models import Product


class Comment(models.Model):
    listing = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', null=True)
    msg = models.TextField(null=True)
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    send_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['send_time']

    def __str__(self):
        return 'Comment {} by {}'.format(self.msg, self.sender)
