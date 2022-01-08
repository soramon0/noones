from django.apps import AppConfig


class ModelsConfig(AppConfig):
    name = 'models'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import models.signals
