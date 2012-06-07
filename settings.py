# Django settings for myproject project.
import os

PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'pybb.Profile'

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('TFBNAME'),
        'USER': os.getenv('TFBNAME'),
        'PASSWORD': os.getenv('TFBPASS'),
        'HOST': '',
        'PORT': '',
    }
}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = PROJECT_ROOT
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_ROOT + '/admin/'
STATICFILES_DIRS = (
	STATIC_ROOT + '/static',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'l^bg09asl1b)#(^7=15sokyg51hriq*e61126lo!h&s*1whbre'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
	'django.template.loaders.app_directories.load_template_source',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

LOGOUT_URL = '/login'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/profile'

ROOT_URLCONF = (
	'myproject.urls'
)

TEMPLATE_DIRS = (
	PROJECT_ROOT + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'registration',
)
CONTEXT_PROCESSORS = (
    'pybb.context_processors.processor',
)
ACCOUNT_ACTIVATION_DAYS = 7
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jtaddei@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAILPASS')
EMAIL_PORT = 587