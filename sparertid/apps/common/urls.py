from django.conf.urls import patterns, include, url

from sparertid.apps.common.views import HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)
