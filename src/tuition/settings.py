import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (('Jayakrishnan Damodaran', 'jayakrishnandforapp1@gmail.com'))
MANAGERS = ADMINS
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Calcutta'
ROOT_URLCONF = 'tuition.urls'

MIDDLEWARE_CLASSES = (
    'tuition.middleware.HandleRequests',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'tuition.common.contextProcessor.contextProcessor',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
)

INSTALLED_APPS = (
    'django.contrib.humanize',
    'tuition.common',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'views'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
)
FILE_CHARSET = 'utf-8'
# https://docs.djangoproject.com/en/1.4/ref/settings/#file-upload-handlers
# only use the memory file uploader, do not use the file system - not able to do so on Google App Engine
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler')

# A secret key for this particular Django installation.
# Used to provide a seed in secret-key hashing algorithms. Set this to a random string -- the longer, the better.
# Do not disclose it
SECRET_KEY = '@anlngdfig$#%$%^&smfldkhdgflhndf__its@my@moneygfad'

DEFAULT_DATE_FORMAT = 'd/m/Y'
DEFAULT_DATE_INPUT_FORMATS = '%d/%m/%Y'
FIRST_DAY_OF_WEEK = 0
MEDIA_ROOT = ''
MEDIA_URL = ''
SITE_ID = 1
USE_I18N = False

# Mark this flag as True if you ever want to prohibit the user activity.
# @see: tuition.middleware.HandleRequests
SITE_DOWN_FOR_MAINTENANCE = False
SITE_DOWN_DESCRIPTION = 'Its My Money is under periodic maintenance and is expected to be down for an hour. <br />\
                         This is to ensure that, we offer the best service, and hence make our site a novel experience for you.'
SITE_SUPPORT_EMAIL = 'care.gcdc.itsmymoney@gmail.com'

IS_DEV_ENV = os.environ['SERVER_SOFTWARE'].startswith('Development')