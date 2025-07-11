from django.apps import AppConfig


class AppadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appAdmin'

    def ready(self):
        import appAdmin.signals
