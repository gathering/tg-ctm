from django.apps import AppConfig


class CtmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ctm'
    
    def ready(self):
        import ctm.signals