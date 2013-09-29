from django.conf.urls import patterns, url

from sparertid.apps.account.views import RegistrationView


urlpatterns = patterns('',
    url(r'^signup/$', RegistrationView.as_view(), name='account_signup'),
)
