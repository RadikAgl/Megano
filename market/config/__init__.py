import settings_app
from config.celery import celery_app as celery_app

__all__ = ("celery_app", "settings_app")
