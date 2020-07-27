from .signals import object_viewed_signal
from django.core.exceptions import ObjectDoesNotExist


class ObjectViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewedMixin, self).get_context_data(*args, **kwargs)
        request = self.request
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return context


    def dispatch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except object_viewed_signal.DoesNotExist:
            instance = None
        if instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return super(ObjectViewedMixin, self).dispatch(request, *args, **kwargs)
