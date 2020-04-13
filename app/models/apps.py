from django.apps import AppConfig


class ModelsConfig(AppConfig):
    name = 'models'

    def ready(self):
        import models.signals
