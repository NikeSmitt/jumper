from .base import *

STATIC_ROOT = 'static/'
STATIC_URL = 'static/'

# Sending email

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
