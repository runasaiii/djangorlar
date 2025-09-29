import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangorlar.settings')

application = get_asgi_application()


assert ENV_ID in ENV_POSSIBLE_OPTIONS, f"Invalid env id. Possible options: {ENV_POSSIBLE_OPTIONS}"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'settings.env.{ENV_ID}')

application = get_asgi_application()