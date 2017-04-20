# encoding: utf-8
"""
Django settings for sm project.

Generated by 'django-admin startproject' using Django 1.8.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '88(f7_b(e=__*@fi=md-=l#_qjh@j8ikje+6uq9wdj&1a_4-%)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sm.djangosite.ocr_api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sm.djangosite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'djangosite.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "webroot/static")
STATIC_ROOT = os.path.join('C:/repos/', "sm_webroot/static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,    
    'disable_existing_loggers': True,    
    'formatters': {        
        'default': {            
            'format': '%(asctime)s %(levelname)s %(message)s'        
        },        
        'simple': {            
            'format': '%(levelname)s %(message)s'        
        },    
    },    
    'handlers': { 
        'console': {            
            'level': 'DEBUG',            
            'class': 'logging.StreamHandler',            
            'formatter': 'simple'        
        }
    },    
    'loggers': {        
        'django.db.backends': {            
            'handlers': ['console'],            
            'level': 'ERROR',            
            'propagate': False,        
        },        
        'django.request': {            
            'handlers': ['console'],            
            'level': 'ERROR',            
            'propagate': True,        
        },    
    },    
    'root': {        
        'handlers': ['console'],        
        'level': 'INFO',    
    }
}


# ocr相关路径配置.
OCR_IMG_INPUT_DIR = 'C:/input/'
OCR_IMG_OUTPUT_DIR = 'C:/output/'
OCR_IMG_OUTPUT_EXTENSIONS = ['.doc', '.pdf', '.xls', '.xlsx']
