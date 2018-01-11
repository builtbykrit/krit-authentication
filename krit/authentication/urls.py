from django.conf.urls import url
from django.views.generic import TemplateView
from .views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmationView,
    UserView,
    UserDetailView,
)

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password/change/', PasswordChangeView.as_view(),
        name='change-password'),
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='reset-password'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmationView.as_view(),
        name='reset-password-confirmation'),

     # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),

    url(r'^users/$', UserView.as_view(), name='users'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailView.as_view(), name='users-detail'),
]