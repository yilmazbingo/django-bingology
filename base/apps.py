from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'
    # configuration for signal
    def ready(self):
        # inorder for this work, in settings.py, we should have our base installed this way: 'base.apps.BaseConfig',
        import base.signals