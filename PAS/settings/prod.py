from .base import *

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['kadpolypms.ng']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

#Email
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL=config('EMAIL_USE_SSL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Media files
STATIC_ROOT = '/home/kadpmhmu/public_html/static'
MEDIA_ROOT = '/home/kadpmhmu/public_html/media'
