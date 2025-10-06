from decouple import config


ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)
ENV_ID = config("DJANGORLAR_ENV_ID", default="local")
SECRET_KEY = config("DJANGO_SECRET_KEY")
