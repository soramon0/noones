from django.apps import AppConfig


class UpdatesConfig(AppConfig):
    name = 'updates'

    def ready(self):
        import updates.signals
