from django.apps import AppConfig


# queueing/apps.py
def ready(self):
    import queueing.signals

class RegistratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registrator'
