from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import \
    validate_password as _validate_password
from rest_framework_json_api import serializers

UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('date_joined', 'email', 'first_name', 'is_staff',
                  'is_superuser', 'is_active', 'last_name',
                  'password')
        read_only_fields = ('date_joined', 'is_active',
                            'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        } # write_only_fields were removed from DRF as of 3.2

    def create(self, validated_data):
        user = UserModel(email=validated_data['email'],
                         first_name=validated_data['first_name'],
                         last_name=validated_data['last_name'],
                         username=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
        _validate_password(password)
        return password
