# krit-authentication
Set of django apps for authentication and registration

This library uses `django-rest-auth`, `djangorestframework`, and `djangorestframework-jsonapi`.

## Getting started

1. Clone this repo
2. Use pip to install dist/krit-authentication-<version>.tar.gz to your project
3. Add `krit-authentication` to your apps
4. Add `krit.authentication.urls` and `krit.registration.urls` to your urlpatterns. Add them to the bottom of the list if you need to override them.

## Usage

### Authentication

**Models**
- User Profile (Abstract)
```
user = models.OneToOneField(
	settings.AUTH_USER_MODEL, related_name='profile',
	on_delete=models.CASCADE, verbose_name="User",
	primary_key=True
)

    class Meta:
        abstract = True
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    class JSONAPIMeta:
        resource_name = "profiles"
```

**Serializers**
- PasswordResetSerializer
- UserSerializer
	- The user serializer just has a meta class that sets the `password` field to `write_only`.

**Views**
- LoginView
- LogoutView
- PasswordChangeView
- PasswordResetConfirmationView
- PasswordResetView
- UserView
- UserDetailView

Most of the time you'll want to subclass the `UserView` and `UserDetailView` to use your own serializers. All of these views use the `JSONAPIRenderer` and `JSONAPIParser`.

**URLS**

If you subclass the `UserView` and `UserDetailView` you'll need to override the `users` and `users-detail` urls to use your custom views. You can do that by using the same url pattern and passing your own custom view.
```
url(r'^users/$', UserView.as_view(), name='users'),
url(r'^users/(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='users-detail')
```

**Settings**
- KRIT_RESET_PASSWORD_URL
- KRIT_RESET_PASSWORD_SUBJECT
- KRIT_SUPPORT_EMAIL_ADDRESS

### Registration

**Models**
- SignupCode
- SignupCodeResult
These models are only used if you are using `krit-teams`


**Serializers**
- UserRegistrationSerializer

**Views**
- UserRegistrationView

**URLS**
- registration

**Settings**
- KRIT_INVITATION_SUBJECT
- KRIT_SIGNUP_URL
