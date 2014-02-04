from os.path import abspath, basename, dirname, join

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ['127.0.0.1', '10.0.0.3', '10.0.0.4', '10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '10.0.0.9']

ADMINS = (
    ('Jonathan Bydendyk', 'jpbydendyk@gmail.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['dev.bushlog.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-ZA'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True
DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d']
TIME_INPUT_FORMATS = ['%I:%M %p', '%H:%M:%S']

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(DJANGO_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(DJANGO_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# List of template context loaders
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware'
)

AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.contrib.flickr.FlickrBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'bushlog.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bushlog.wsgi.application'

TEMPLATE_DIRS = (
    join(DJANGO_ROOT, "templates"),
)

INSTALLED_APPS = (

    # required django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # django admin over-ride apps
    'suit',

    # django admin apps
    'django.contrib.admin',
    'django.contrib.admindocs',

    # reusable apps
    'compressor',
    'gunicorn',
    'rest_framework',
    'rest_framework.authtoken',
    'social_auth',
    'south',

    # project specific apps
    'bushlog',
    'bushlog.apps.action',
    'bushlog.apps.location',
    'bushlog.apps.profile',
    'bushlog.apps.reserve',
    'bushlog.apps.sighting',
    'bushlog.apps.wildlife',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

# CSRF settings
CSRF_FAILURE_VIEW = 'bushlog.views.csrf_failure'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 60 * 24 * 14,  # 14 day default
    }
}

# Compressor settings
COMPRESS_OUTPUT_DIR = 'cache'

# Comment settings
PROFANITIES_LIST = [w.strip() for w in open(join(STATIC_ROOT, 'badwords.txt')).readlines()]

# Email settings
FROM_EMAIL = "Bushlog <info@bushlog.com>"

# Extends the standard django user object
AUTH_PROFILE_MODULE = 'bushlog.apps.profile.UserProfile'

# Social auth user defined redirects
SOCIAL_AUTH_INACTIVE_USER_URL = '/profile/inactive/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/profile/associate/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/profile/associate/'

# Social auth pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

# Social auth exception handling via messages
SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'social_auth.utils.log_exceptions_to_messages'

# Social auth login urls
LOGIN_URL = '/profile/signin/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'
IGNOREABLE_WORDS = [
    'african',
    'plains',
    'antelope',
    'southern',
    'chacma',
    'common',
    'spotted',
    'nile'
]

# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'PAGINATE_BY': 20,
    'PAGINATE_BY_PARAM': 'page_size'
}
