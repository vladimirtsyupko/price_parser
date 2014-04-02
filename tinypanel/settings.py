"""
Django settings for tinypanel project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1fa+h4f+&s2(c_4y98d$5ljq_jvwk#0$wa++1e713nx8vh7_rc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'south',
    'helper',
    'airlines_parser',
    'prices_parser',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tinypanel.urls'

WSGI_APPLICATION = 'tinypanel.wsgi.application'
DEBUG = True
DOWNLOAD_DELAY = 10
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
ALLOWED_HOSTS = []
MEDIA_ROOT = BASE_DIR + u'/media'
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
ON_SERVER = False
# product parser
DB_USE = 'mysql'
#DB_USE = 'sqlite'
# DB_USE = 'gdrive'
GDRIVE_EMAIL = 'nick.j.samuel@gmail.com'
GDRIVE_PASS = 'tvsbzhtftikudvut'
GDRIVE_FILE = 'test'

SQLITE_PATH = r'f:\sqlite\django.db'

# used for Staples in product parser
LOCATION = '10001'
if ON_SERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tinypanel',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost'
        }
    }
    MYSQL_USER_HOST = 'localhost'
    MYSQL_USER_LOGIN = 'root'
    MYSQL_USER_PASSWD = ''
    MYSQL_USER_DB = 'tinypanel'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tinypanel',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost'
        }
    }
    MYSQL_USER_HOST = 'localhost'
    MYSQL_USER_LOGIN = 'root'
    MYSQL_USER_PASSWD = ''
    MYSQL_USER_DB = 'tinypanel'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = "/static/"
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
)