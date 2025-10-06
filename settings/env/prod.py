from settings.base import *
import os
from settings.base import BASE_DIR


ROOT_URLCONF = "settings.urls"
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
