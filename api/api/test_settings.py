from .settings import *

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = ()
