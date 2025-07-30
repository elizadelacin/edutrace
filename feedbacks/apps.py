from django.apps import AppConfig


class AssessmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedbacks'

    def ready(self):
        import feedbacks.signals