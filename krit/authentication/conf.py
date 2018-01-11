from __future__ import unicode_literals

from appconf import AppConf


class KritAuthenticationAppConf(AppConf):

    KRIT_RESET_PASSWORD_URL = ""
    KRIT_RESET_PASSWORD_SUBJECT = ""
    KRIT_SUPPORT_EMAIL_ADDRESS = ""
    REST_AUTH_SERIALIZERS = {
        'PASSWORD_RESET_SERIALIZER': 'krit.authentication.serializers.PasswordResetSerializer',
    }
    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework_json_api.parsers.JSONParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.MultiPartParser'
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_json_api.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    class Meta:
        prefix = "krit_authentication"