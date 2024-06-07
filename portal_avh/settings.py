"""
Django settings for portal_avh project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rl(lh-nmmvpj_gp(q+wb954=zy%)g9e^^0i_*=-6u3g#ah)a5*"
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
DATA_UPLOAD_MAX_NUMBER_FILES = None
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", "portal.avh.kz"]
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "http://portal.avh.kz",
    "https://portal.avh.kz",
    "http://localhost:*",
    "http://10.10.20.13:*",
]
X_FRAME_OPTIONS = "SAMEORIGIN"

DEFAULT_AUTHENTICATION_CLASSES = [
    "rest_framework.authentication.SessionAuthentication",
    "rest_framework.authentication.BasicAuthentication",
]
# Application definition

LOGIN_URL = "/login/"
COMPRESSION_QUALITY = 85
MAX_UPLOAD_SIZE = 15 * 1024 * 1024

INSTALLED_APPS = [
    "admin_global_search",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "colorfield",
    "simple_history",
    "djmoney",
    # Основная
    "main",
    # Дополнительные сервисы
    "avh_modules",
    "egov_modules",
    "api",
    # DEV ветки
    "anu",
    "mp",
    "np",
    "gp",
    "p1",
    "p2",
    # mp's apps
    "calculator",
    "doctrack",
    "notifications",
    "document_debts",
    # p1's apps
    "tester_atp_avr",
    "documents",
    "pdf_compressor",
    "corsheaders",
    "rest_framework",
    "order_entry_as_html",
    "visual_deadline",
    "reporter",
    "import_generator_by_maw",
    "calculator_emr",
    "constructor_do",
    "contract_report",
    "order_generator_by_kcell",
    "widget_tweaks",
    "designer_requests_for_equipment",
    "finance_module",
    "finance_module.for_treasurers",
    "finance_module.mandatory_payments",
    # Yernur's apps
    "report_kartel",
    "handbook_bekzhan",
    "finance_module.division_of_financial_planning",
    "finance_module.unpaid_invoices",
    "Security_Department",
    "nomenclature",
    "google_to_html",
    "pdf_to_json_for_1c",
    "json_to_excel",
    "add_docnum",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

ROOT_URLCONF = "portal_avh.urls"

AUTH_USER_MODEL = "main.AvhUser"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Указываем путь к папке templates
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.context_processors.chapters",
                "finance_module.context_processors.finance_sections"
            ],
            "libraries": {
                "to_dot": "calculator.templatetags.to_dot",
                "to_float": "calculator.templatetags.to_float",
            },
        },
    },
]
STATIC_URL = "/static/"  # URL, по которому будут доступны статические файлы
STATICFILES_DIRS = [
    os.path.join(
        BASE_DIR, "static"
    )  # Путь к папке с вашими статическими файлами (HTML, CSS, JS)
]

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

AUTH_USER_MODEL = "main.AvhUser"
LOGIN_REDIRECT_URL = "/"

WSGI_APPLICATION = "portal_avh.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRESQL_NAME"),
        "USER": os.getenv("POSTGRESQL_USER"),
        "PASSWORD": os.getenv("POSTGRESQL_PASSWORD"),
        "PORT": os.getenv("POSTGRESQL_PORT"),
        "HOST": os.getenv("POSTGRESQL_HOST"),
    },
    "report_kartel_db": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_for_website.sqlite3",
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"
DEFAULT_CURRENCY = "KZT"
TIME_ZONE = "Asia/Almaty"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_PORT = 3636
EMAIL_USE_TSL = True
EMAIL_HOST = "mailgate.avh.kz"
EMAIL_HOST_USER = "portal@group.kz"
EMAIL_HOST_PASSWORD = "@WSX3edc"
DEFAULT_FROM_EMAIL = "portal@avh.kz"

DEFAULT_FILE_STORAGE = "portal_avh.system_models.CustomFileSystemStorage"

CELERY_BROKER_URL = "redis://localhost:6379"  #'pyamqp://guest:guest@localhost:5672//'

CELERY_TIMEZONE = "Asia/Almaty"
# CELERY_RESULT_BACKEND = 'django-db'


INSTALLED_APPS += [
    "celery",
    "django_celery_beat",
    "django_celery_results",
    "mathfilters",
]

DATE_INPUT_FORMATS = [
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H:%M",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%d.%m.%Y",
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%d.%m.%y",
]

CELERY_BEAT_SCHEDULE = {  # scheduler configuration
    "update_data_for_calculator": {  # whatever the name you want
        "task": "calculator.tasks.auto_updates",  # name of task with path
        "schedule": crontab(
            minute=32, hour=8, day_of_week="1-5"
        ),  # crontab() runs the tasks every minute
    },
    "update_data_for_19_45": {  # whatever the name you want
        "task": "calculator.tasks.auto_updates_19_45",  # name of task with path
        "schedule": crontab(
            minute=50, hour=8, day_of_week="1-5"
        ),  # crontab() runs the tasks every minute
    },
    "update_data_for_damir": {  # whatever the name you want
        "task": "calculator.tasks.read_and_read_json",  # name of task with path
        "schedule": crontab(minute=20, hour=9),  # crontab() runs the tasks every minute
    },
    "update_data_for_emr_bs": {  # whatever the name you want
        "task": "calculator.tasks.auto_updates_for_emr",  # name of task with path
        "schedule": crontab(
            minute=35, hour=9, day_of_week="1-5"
        ),  # crontab() runs the tasks every minute
    },
    "auto_updates_7_11_2": {  # whatever the name you want
        "task": "calculator.tasks.auto_updates_7_11_2",  # name of task with path
        "schedule": crontab(
            minute=3, hour=7, day_of_week="1-5"
        ),  # crontab() runs the tasks every minute
    },
    "auto_updates_19_22": {  # whatever the name you want
        "task": "calculator.tasks.auto_updates_19_22",  # name of task with path
        "schedule": crontab(minute=55, hour=9, day_of_week='1-5'),  # crontab() runs the tasks every minute
    },
    "import_unpaid_invoices1": {
        "task": "finance_module.tasks.import_unpaid_invoices_shared_task",
        "schedule": crontab(hour=11, minute=45),
    },
    "import_unpaid_invoices2": {
        "task": "finance_module.tasks.import_unpaid_invoices_shared_task",
        "schedule": crontab(hour=15, minute=45),
    },
    # "task_debt_on_doc_for_dima": {  # whatever the name you want
    #     "task": "calculator.tasks.debt_on_doc_for_dima",  # name of task with path
    #     "schedule": crontab(
    #         0, 0, day_of_month="3"
    #     ),  # crontab() runs the tasks every minute
    # },
}

BACKGROUND_TASK_RUN_ASYNC = True