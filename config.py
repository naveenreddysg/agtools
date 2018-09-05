import os
from datetime import timedelta

debug_config = True
basedir = os.path.abspath(os.path.dirname(__file__))

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
BCRYPT_LOG_ROUNDS = 13
BCRYPT_HASH_PREFIX = '2a'

ASSETS_DEBUG = False
DEBUG_TB_ENABLED = False  # Disable Debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False
LOG_RESPONSE = True


WTF_CSRF_ENABLED = True
ADMINS = ['hughson.simon@gmail.com']
MANAGERS = ADMINS

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://agtool_dev:agtool123@10.6.52.71/agtools_ui"
SQLALCHEMY_BINDS = {
    'db1': SQLALCHEMY_DATABASE_URI
    #'db2': 'mysql://db_user:db_pw@localhost:3306/db_name'
}
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

PERMANENT_SESSION_LIFETIME = timedelta(minutes=1200)

TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = '\xcb\xe2\xaf%\xaeV(\xf9S\xa1\xa1\x90\xf5\xfd>\xdey\x18\x8f04\xfa\xed\x84'

MAIL_SERVER = 'mail.smtp2go.com'
MAIL_PORT = 2525  # 8025, 587 and 25 can also be used.
MAIL_USE_TSL = True
MAIL_USERNAME = 'hughson.simon@gmail.com'
MAIL_PASSWORD = 'N2L1A6lSAZEp'
MAIL_DEFAULT_SENDER = 'support@ag.tools'

STRIPE_PUBLIC_KEY = 'pk_live_45ReJuOvb13kbGNZMOWH387Q'
STRIPE_SECRET_KEY = 'sk_live_pGUCOxgW15L6xqxv7ezeKcZH'



INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "analysis"


)





