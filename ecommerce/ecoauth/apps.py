from django.apps import AppConfig


class EcoauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecoauth'
    def ready(self):
        import ecoauth.signals
        
