from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import \
    validate_password as _validate_password
from rest_framework_json_api import serializers

UserModel = get_user_model()


def _get_user_registration_fields():
    """Return fields to serialize from UserModel"""
    if type(UserModel.__dict__.get('registration_fields')) == tuple:
        return UserModel.registration_fields
    return ('date_joined', 'email', 'first_name', 'is_staff',
            'is_superuser', 'is_active', 'last_name',
            'password')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = _get_user_registration_fields()
        read_only_fields = ('date_joined', 'is_active',
                            'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        } # write_only_fields were removed from DRF as of 3.2

    def create(self, validated_data):
        user = UserModel(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
        _validate_password(password)
        return password
