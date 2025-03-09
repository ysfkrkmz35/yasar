# Merged File: apps.py

from django.apps import AppConfig

class EntityConfig(AppConfig):
    name = 'entity'
    verbose_name = 'Tablolar'

    def ready(self):
        pass

# From Meetings Folder:

from django.apps import AppConfig

class MeetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Django 3.2+ için otomatik alan tipi
    name = 'meetings'  # Uygulama adı
    path = '/home/cemtakak/yasar/meetings'


