from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView

from sparertid.apps.account.models import User
from sparertid.apps.account.forms import UserCreationForm


class RegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        resp = super(RegistrationView, self).form_valid(form)

        user = authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        return resp
