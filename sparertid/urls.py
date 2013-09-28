from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sparertid.apps.imbot.views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
