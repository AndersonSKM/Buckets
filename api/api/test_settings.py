from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = ()

LOGGING['loggers']['django']['level'] = 'ERROR'
LOGGING['loggers']['gunicorn']['level'] = 'ERROR'

DJOSER['SEND_ACTIVATION_EMAIL'] = True
