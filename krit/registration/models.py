from __future__ import unicode_literals

import operator

from django.contrib.sites.models import Site
try:
    from django.core.urlresolvers import reverse
except ModuleNotFoundError:
    from django.urls import reverse
from django.db import models
from django.utils import timezone
from functools import reduce
from urllib.parse import urlencode

from django.conf import settings
from .hooks import hookset
from .signals import signup_code_sent, signup_code_used


class SignupCode(models.Model):

    class AlreadyExists(Exception):
        pass

    class InvalidCode(Exception):
        pass

    code = models.CharField("code", max_length=64, unique=True)
    created = models.DateTimeField("created", default=timezone.now, editable=False)
    email = models.EmailField(max_length=254, blank=True)
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True, blank=True,
                                on_delete=models.CASCADE)
    sent = models.DateTimeField("sent", null=True, blank=True)

    class JSONAPIMeta:
        resource_name = "signup_codes"

    class Meta:
        verbose_name = "signup code"
        verbose_name_plural = "signup codes"

    def __str__(self):
        if self.email:
            return "{0} [{1}]".format(self.email, self.code)
        else:
            return self.code

    @classmethod
    def exists(cls, code=None, email=None):
        checks = []
        if code:
            checks.append(models.Q(code=code))
        if email:
            checks.append(models.Q(email=code))
        if not checks:
            return False
        return cls._default_manager.filter(
            reduce(operator.or_, checks)).exists()

    @classmethod
    def create(cls, **kwargs):
        email, code = kwargs.get("email"), kwargs.get("code")
        if kwargs.get("check_exists", True) and cls.exists(code=code, email=email):
            raise cls.AlreadyExists()
        if not code:
            code = hookset.generate_signup_code_token(email)
        params = {
            "code": code,
        }
        if email:
            params["email"] = email
        if kwargs.get("inviter", None):
            params["inviter"] = kwargs.get("inviter")
        return cls(**params)

    @classmethod
    def check_code(cls, code):
        try:
            signup_code = cls._default_manager.get(code=code)
        except cls.DoesNotExist:
            raise cls.InvalidCode()
        else:
            return signup_code

    def use(self, user):
        """
        Add a SignupCode result attached to the given user.
        """
        result = SignupCodeResult()
        result.signup_code = self
        result.user = user
        result.save()
        signup_code_used.send(sender=result.__class__, signup_code_result=result)

    def send(self, **kwargs):
        if hasattr(settings, "KRIT_SIGNUP_URL"):
            signup_url = "{}?{}".format(
                settings.KRIT_SIGNUP_URL,
                urlencode({"code": self.code})
            )
        elif "signup_url" not in kwargs:
            protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
            current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
            signup_url = "{0}://{1}{2}?{3}".format(
                protocol,
                current_site.domain,
                reverse("registration"),
                urlencode({"code": self.code})
            )
        else:
            signup_url = kwargs["signup_url"]
        ctx = {
            "signup_code": self,
            "signup_url": signup_url,
        }
        ctx.update(kwargs.get("extra_ctx", {}))
        hookset.send_invitation_email(self.email, ctx)
        self.sent = timezone.now()
        self.save()
        signup_code_sent.send(sender=SignupCode, signup_code=self)


class SignupCodeResult(models.Model):

    signup_code = models.ForeignKey(SignupCode, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
