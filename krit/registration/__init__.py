import pkg_resources


__version__ = pkg_resources.get_distribution("krit-authentication").version
default_app_config = "krit.registration.apps.AppConfig"
