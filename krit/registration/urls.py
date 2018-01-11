from django.conf.urls import url
from .views import UserRegistrationView

urlpatterns = [
    url(r'^$', UserRegistrationView.as_view(), name='registration'),
]
