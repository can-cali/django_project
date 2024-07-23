from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        # we are importing signals here to avoid circular imports.
        # This is the recommended way to import signals in Django.
        # https://docs.djangoproject.com/en/3.2/topics/signals/#connecting-receiver-functions