from django.views.generic import CreateView

class ProjectCreateView(CreateView):
	template_name = "project/create"
	success_url = '/'

