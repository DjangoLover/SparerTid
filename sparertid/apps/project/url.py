from django.conf.urls import patterns, url


urlpatterns = patterns('project.views',
	url('create/', view, name='create-project')
)