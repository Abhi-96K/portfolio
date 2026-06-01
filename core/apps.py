from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Import inside ready() to avoid AppRegistryNotReady during startup
        from django.contrib.auth.models import update_last_login
        from django.contrib.auth.signals import user_logged_in

        # Disconnect last_login update using its dispatch_uid to allow admin logins on Vercel's read-only SQLite database.
        user_logged_in.disconnect(update_last_login, dispatch_uid="update_last_login")




