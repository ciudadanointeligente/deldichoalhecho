"""
Django settings for deldichoalhecho_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
import sys

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY','s3cret0')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in os.environ and os.environ.get('DEBUG') == 1

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'adminsortable2',
    'picklefield',
    'popolo',
    'constance',
    'constance.backends.database',
    'django_extensions',
    'django_nose',
    'taggit',
    'promises',
    'deldichoalhecho_theme',
    'instances',
    'promises_instances',
    'ddah_web',
    'promises_forms',
    'backend',
    'django_ace',
    'ddah_admin_section',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'instances.middleware.MultiInstanceMiddleware',
    'ddah_web.middleware.DDAHSiteMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project_site.subdomain_urls'
ROOT_URLCONF_HOST = 'project_site.non_subdomain_urls'

WSGI_APPLICATION = 'project_site.wsgi.application'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TESTING = 'test' in sys.argv

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

SITE_ID = 1

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#CONSTANCE
CONSTANCE_CONFIG = {'LANDING_PHRASE': ("Del dicho al hecho", 'the landing phrase for the site'),
                    'DESCRIPTION_PHRASE': ("Promise tracking site", 'the description of the site'),
                    'GOOGLE_ANALYTICS': ("UA-XXXXXXX-X", "Google analytics code "),
                    'DISQUS_SHORTCODE': ("disqusshortcode", "Disqus shortcode"),
                    'CURRENT_THEME': ("base", "Current theme"),
                    'OG_IMAGE': ("https://raw.githubusercontent.com/ciudadanointeligente/check-it/100dias/deldichoalhecho_theme/100dias/static/img/logo-og.png",
                        "Image to be displayed for OG"),
                    }

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "constance.context_processors.config")

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)
# MultiInstance Thing

BASE_HOST = os.environ.get('BASE_HOST', '127.0.0.1.xip.io:8000')
#HEROKU SPECIFICS
# Parse database configuration from $DATABASE_URL
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'deldichoalhecho_theme', 'edicion2015', 'static'),
    os.path.join(BASE_DIR, '..', 'backend', 'static'),
    os.path.join(BASE_DIR, '..', 'ddah_web', 'static'),
)

# EXTRA TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)
# END OF HEROKU SPECIFICS

#LOGGING
LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
                    'simple':   {'format': '%(asctime)s %(levelname)s %(message)s'},
                },
        'handlers': {
                    'console':     {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'simple'},
                    'null': {
                                    'level': 'DEBUG',
                                    'class': 'logging.NullHandler',
                                },
                },
        'loggers': {
                    'django.db.backends': {'level': 'DEBUG', 'handlers': ['null'], 'propagate': False},
        }
}
#END LOGGING
#Testing without migrations
from django.conf import settings
from django_nose import NoseTestSuiteRunner


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


class Runner(NoseTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None):
        settings.MIGRATION_MODULES = DisableMigrations()
        super(Runner, self).run_tests(test_labels, extra_tests=extra_tests)


DONT_USE_MIGRATIONS = 'DONT_USE_MIGRATIONS' in os.environ.keys() and os.environ['DONT_USE_MIGRATIONS'] == '1'

if DONT_USE_MIGRATIONS:
    TEST_RUNNER = 'project_site.settings.Runner'

# DEFAULT SETTINGS
DEFAULT_SOCIAL_NETWORKS={
    "twitter_text": "Mira que lindo mi sitio",
    "og_img": "http://placehold.it/400x400"
}
DEFAULT_STYLE={
    "header_img": "http://i.imgur.com/7ULzGlP.png",
    "background_color": "0F2356",
    "second_color": "0F0F28",
    "read_more_color": "750661"
}
if TESTING:
    CELERY_ALWAYS_EAGER = True
CELERY_ALWAYS_EAGER = True
# END DEFAULT SETTINGS
try:
    from local_settings import *
except ImportError:
    pass
