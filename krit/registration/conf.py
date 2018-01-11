import importlib

# Import settings from django.conf before
# importing appconf.AppConf
# https://pypi.python.org/pypi/django-appconf
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from appconf import AppConf

def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


class RegistrationAppConf(AppConf):

    HOOKSET = "krit.registration.hooks.RegistrationDefaultHookset"
    KRIT_INVITATION_SUBJECT = ""
    KRIT_SIGNUP_URL = ""

    def configure_hookset(self, value):
        return load_path_attr(value)()
