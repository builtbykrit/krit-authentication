from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_json_api import renderers

from .hooks import hookset
from .models import SignupCode
from .serializers import UserRegistrationSerializer

MESSAGE_STRINGS = hookset.get_message_strings()


class UserRegistrationView(CreateAPIView):
    model = User
    renderer_classes = (renderers.JSONRenderer,)
    resource_name = 'users'
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        try:
            signup_code = request.data.get('code', None)
            if signup_code:
                signup_code = SignupCode.check_code(signup_code)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            user = serializer.instance

            if signup_code:
                signup_code.use(user)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        except SignupCode.InvalidCode:
            raise ValidationError(MESSAGE_STRINGS["invalid_signup_code"])
        except IntegrityError as e:
            str_e = str(e)
            if "Key (username)=(" in str_e and ") already exists." in str_e:
                raise ValidationError(MESSAGE_STRINGS["duplicate_email"])
            else:
                raise APIException(str_e)
