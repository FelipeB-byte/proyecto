import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DEBUG = env.bool('DEBUG', default=True)
SECRET_KEY = env('SECRET_KEY', default='dev-secret')
ALLOWED_HOSTS = [h.strip() for h in env('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'reservas'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'canchas.urls'

TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/'reservas'/'templates', BASE_DIR/'templates'],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages'
    ]},
}]

WSGI_APPLICATION = 'canchas.wsgi.application'

import pymysql
pymysql.install_as_MySQLdb()


DATABASES = {
    'default': {
        'ENGINE':   env('DB_ENGINE',   default='django.db.backends.mysql'),
        'NAME':     env('DB_NAME',     default='canchas_db'),
        'USER':     env('DB_USER',     default='root'),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'HOST':     env('DB_HOST',     default='127.0.0.1'),
        'PORT':     env('DB_PORT',     default='3306'),
        'OPTIONS':  {'charset': 'utf8mb4'},
    }
}

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR/'reservas'/'static']
STATIC_ROOT = BASE_DIR/'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

OPEN_HOUR = env.int('OPEN_HOUR', default=18)
CLOSE_HOUR = env.int('CLOSE_HOUR', default=22)
RESERVA_INTERVAL_MINUTES = env.int('RESERVA_INTERVAL_MINUTES', default=60)
