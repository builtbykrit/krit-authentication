from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class UserProfile(models.Model):
    """
    A model to store a user's settings
    """
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
