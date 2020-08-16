import os
from eCommerce_Django.utils import get_secret_key


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = get_secret_key(BASE_DIR, 'SECRET_KEY')

DEBUG = True

DJANGO_TEST_PROCESSES = 8

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',

    'django.contrib.admin',
    'django.contrib.auth',

    'addresses',
    'analytics',
    'billing',
    'products',
    'carts',
    'marketing',
    'orders',
    'search',
    'tags',
    'chats',
]


SUPPORT_EMAIL = get_secret_key(BASE_DIR, 'SUPPORT_EMAIL')

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = SUPPORT_EMAIL
EMAIL_HOST_PASSWORD = get_secret_key(BASE_DIR, 'EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SUPPORT_EMAIL
MANAGERS = (
    ('Nikita', SUPPORT_EMAIL),
)
ADMINS = MANAGERS


BASE_URL = '127.0.0.1:8000'


MAILCHIMP_API_KEY = get_secret_key(BASE_DIR, 'MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = 'us10'
MAILCHIMP_EMAIL_LIST_ID = get_secret_key(BASE_DIR, 'MAILCHIMP_EMAIL_LIST_ID')
MAILCHIMP_EMAIL_ADMIN = get_secret_key(BASE_DIR, 'MAILCHIMP_EMAIL_ADMIN')

STRIPE_SECRET_KEY = get_secret_key(BASE_DIR, 'STRIPE_SECRET_KEY')
STRIPE_PUB_KEY = get_secret_key(BASE_DIR, 'STRIPE_PUB_KEY')

PAYPAL_CLIENT_ID = get_secret_key(BASE_DIR, 'PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = get_secret_key(BASE_DIR, 'PAYPAL_CLIENT_SECRET')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


LOGOUT_REDIRECT_URL = '/login/'
ROOT_URLCONF = 'eCommerce_Django.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eCommerce_Django.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_COOKIE_SAMESITE = 'Lax'

LOCALE_PATHS = [ os.path.join(BASE_DIR, 'locale'), ]

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'ru'

LANGUAGES = [ ('en', 'English'), ('ru', 'Russian'), ]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static_my_proj"),]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")

PROTECTED_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "protected_media")
