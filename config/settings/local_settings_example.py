SECRET_KEY = ""
DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "web_diarization",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

PYANNOTE_AUTH_TOKEN = ""
CHAT_GPT_API_KEY = ""
CELERY_BROKER_URL = "redis://localhost:6379"
