from django.contrib.auth.forms import PasswordResetForm as RestAuthPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from python_http_client.exceptions import BadRequestsError
from django.conf import settings
from urllib.parse import urlencode


class PasswordResetForm(RestAuthPasswordResetForm):
    def send_mail(self, context, to_email):

        token = context["token"]
        uid = context["uid"]
        password_reset_url = None
        if hasattr(settings, "KRIT_RESET_PASSWORD_URL"):
            password_reset_url = "{}?{}".format(
                settings.KRIT_RESET_PASSWORD_URL,
                urlencode({"token": token, "uid": uid}))
        mail = EmailMultiAlternatives(
            from_email=settings.KRIT_SUPPORT_EMAIL_ADDRESS,
            reply_to=[settings.KRIT_REPLY_TO_EMAIL_ADDRESS],
            to=to_email
        )
        mail.template = 'reset-password'
        mail.substitution_data = {'link': password_reset_url}

        try:
            mail.send()
        except BadRequestsError as e:
            print(e.reason)
            raise e

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(context, [email])
