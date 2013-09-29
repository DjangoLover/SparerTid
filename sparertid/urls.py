from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('sparertid.apps.common.urls')),
    url(r'^account/', include('sparertid.apps.account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^project/', include('sparertid.apps.project.urls')),
)
