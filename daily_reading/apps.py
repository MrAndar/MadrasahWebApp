from django.apps import AppConfig


class DailyReadingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_reading'

    def ready(self):
        import daily_reading.templatetags.custom_tags
