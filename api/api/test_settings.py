from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = ()

LOGGING['loggers'].pop('django')
LOGGING['loggers'].pop('gunicorn')

DJOSER['SEND_ACTIVATION_EMAIL'] = True

WHITENOISE_AUTOREFRESH = True
