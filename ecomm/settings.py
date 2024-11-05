import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#load our environment variables
load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-agu4_-w2cuqvi+3ipby2q773*7*j7^37dsw5ylzhf%to-ts$j7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['localhost','87d3-223-185-132-168.ngrok-free.app']
ALLOWED_HOSTS = ['localhost','e9fb-223-185-132-168.ngrok-free.app','127.0.0.1']
ngrok_url = "https://e9fb-223-185-132-168.ngrok-free.app"
CSRF_TRUSTED_ORIGINS = [ngrok_url]
#CSRF_COOKIE_SECURE = True# Only send the CSRF cookie over HTTPS
#CSRF_COOKIE_SAMESITE = 'Lax'  # Adjust the SameSite attribute as per your needs

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'shoppingcart',
    'payment',
    'whitenoise.runserver_nostatic',
    'paypal.standard.ipn',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecomm.urls'
#CSRF_COOKIEDOMAIN = None
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shoppingcart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        #'HOST':'viaduct.proxy.rlwy.net',
        'HOST':'junction.proxy.rlwy.net',
        'PORT': '33719',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =[
                   os.path.join(BASE_DIR,'static')
                   ]
STATIC_ROOT = os.path.join(BASE_DIR , 'staticfiles')

#White noise static things
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR/'staticfiles'


MEDIA_URL = 'media/'
MEDIA_ROOT =os.path.join(BASE_DIR,'/media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Adding PayPal Settings Here
#Set sandbox to true as in the documentation -https://django-paypal.readthedocs.io/en/latest/standard/ipn.html
PAYPAL_TEST = True

#set the sandbox business email account to paypal receiver email
PAYPAL_RECEIVER_EMAIL = 'personaldjangotest@gmail.com'
