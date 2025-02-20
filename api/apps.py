from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """Connect signals instead of accessing the database directly."""
        import api.signals  # Import signals when app is ready
