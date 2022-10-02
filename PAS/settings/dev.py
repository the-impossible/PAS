from .base import *

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_SSL=True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply.kadpolypms@gmail.com'
EMAIL_HOST_PASSWORD = 'pnrmqwlxrposswyt'

# EMAIL_HOST_USER = 'richardemmanuel45@gmail.com'
# EMAIL_HOST_PASSWORD = 'kqrbbzylrxqpwbmn'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'Static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
