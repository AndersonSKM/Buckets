from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = ()

LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['gunicorn']['level'] = 'INFO'
LOGGING['loggers']['']['level'] = 'INFO'

DJOSER['SEND_ACTIVATION_EMAIL'] = True
