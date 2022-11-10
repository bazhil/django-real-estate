from __future__ import absolute_import
import os

from celery import Celery
from real_estate import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate.settings')

app = Celery('real_estate')

app.config_from_object('real_estate.settings', namespace='CELERY')

app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

