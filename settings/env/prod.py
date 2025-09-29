import os
from settings.base import BASE_DIR  # import only what is needed

DEBUG = False
ALLOWED_HOSTS = ["*"]  # или список доменов/айпи, где проект будет работать

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
