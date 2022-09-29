"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os, environ

from pathlib import Path
from django.urls import reverse_lazy

from django.contrib.messages import constants as messages_constants

MESSAGE_LEVEL = messages_constants.DEBUG

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Application definition

VENDOR_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_summernote',
    'multiselectfield',
    'markdownx',
    'compressor',
    'notifications',
]

LOCAL_APPS = [
    'accountapp',
    'teamapp',
    'subscribeapp',
    'commentapp',
    'contestapp',
    'notificationapp',
    'chatapp',
]

INSTALLED_APPS = VENDOR_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.CheckAuthMiddleware',
    # 'middleware.NoteMiddleware' # 리뉴얼공지
]

ROOT_URLCONF = 'website.urls'

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

WSGI_APPLICATION = 'website.wsgi.application'

# SESSION CONFIGURATION

SESSION_COOKIE_AGE = 43200 # 12 hours
SESSION_SAVE_EVERY_REQUEST = True


# Password email
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # media 지정되는 경로

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTH, MIDDLEWARE Settings

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

LOGIN_URL = reverse_lazy('account:login')
LOGIN_REDIRECT_URL = reverse_lazy('account:index')
LOGOUT_REDIRECT_URL = reverse_lazy('account:index')
PROFILE_CREATE_URL = reverse_lazy('account:create')
INDEX_URL = reverse_lazy('account:index')
NOTE_URL = reverse_lazy('account:note') # 공지

LOGIN_EXEMPT_URLS = (
    r'^signup/$',
    r'^$',
    r'^account/activate/.*/.*$',
    r'^members/$',
    r'^teams/$',
    r'^teams/[0-9]*/$',
    r'^teams/comment/[0-9]*/$',
    r'^media/.*$',
    r'^comment/team/[0-9]*/$',
    r'^subscribe/team/$',
    r'^autocomplete/.*$',
    r'^intro/$',
    r'^contest/$',
    r'^contest/[0-9]*/$',
    r'^contest/comment/[0-9]*/$',
    r'^comment/contest/[0-9]*/$',
    r'^subscribe/contest/$',
    r'^findaccount/$',
    r'^findid/$',
    r'^findid/verified/.*$',
    r'^findpw/$',
    r'^findpw/verified/.*$',
    r'^findpw/sent/$',
    r'^findpw/complete/$',
    r'^robots.txt/$',
    r'^sitemap.xml/$',
    r'^note/$',
)

PROFILE_EXEMPT_URLS = (
    r'^profile/create/$',
)

ADMIN_URLS = (
    r'^admin/*',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'accountapp.User'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# SUMMERNOTE SETTINGS

SUMMERNOTE_CONFIG = {
    'attachment_filesize_limit': 10 * 1024 * 1024,
    'iframe': True,
    'summernote': {
        'width': '100%',
        'height': '540',
        'fontSizes': ['10','11','12','14','16','18','24','36','40'],
        'toolbar': [
            ['font', ['bold', 'underline', 'strikethrough','clear']],
            ['color', ['color']],
            ['fontsize', ['fontsize']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['undo', ['undo', ]],
            ['redo', ['redo', ]],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'help']],
        ],
        'lang': 'ko-KR',
    },
    'attachment_require_authentication': True,
}

# MARKDOWNX SETTINGS

# Django JET

JET_SIDE_MENU_COMPACT = True
JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'deploy/config/client_secrets.json')

# Django Compressor

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True
# EMAIL CONFIGURATION

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'from.devdreamer@gmail.com'
EMAIL_HOST_PASSWORD = 'dreaming1234'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '꿈꾸는개발자 <%s>' % EMAIL_HOST_USER
