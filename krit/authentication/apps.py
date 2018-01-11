from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'krit.authentication'
    label = "krit_authentication"
