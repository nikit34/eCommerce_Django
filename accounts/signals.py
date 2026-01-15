from django.dispatch import Signal


# providing_args was removed in Django 4.0
# Signal now accepts no arguments (args are documented but not enforced)
user_logged_in = Signal()
