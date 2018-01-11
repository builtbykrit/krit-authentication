from django.contrib.auth import get_user_model
from rest_framework_json_api import serializers
from rest_auth.serializers import PasswordResetSerializer as RestAuthPasswordResetSerializer

from .forms import PasswordResetForm

UserModel = get_user_model()


class PasswordResetSerializer(RestAuthPasswordResetSerializer):
    password_reset_form_class = PasswordResetForm


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }  # write_only_fields were removed from DRF as of 3.2

