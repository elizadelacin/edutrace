from django.apps import AppConfig


class AssessmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homeworks'

    def ready(self):
        import homeworks.signals