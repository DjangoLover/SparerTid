from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from sparertid.lib.forms import FieldAttributesFormMixin
from .models import User


class UserCreationForm(FieldAttributesFormMixin, forms.ModelForm):

    widget_attrs = {
        'email': {'class': 'form-control'},
        'jid': {'class': 'form-control'},
        'timezone': {'class': 'form-control'},
        'password1': {'class': 'form-control'},
        'password2': {'class': 'form-control'},
    }

    password1 = forms.CharField(
        label=_('Password'),
        max_length=15, min_length=6,
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        max_length=15, min_length=6,
        widget=forms.PasswordInput
    )

    class Meta():
        model = User
        fields = ('email', 'jid', 'timezone')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')

        if password1 and password1 != self.cleaned_data['password2']:
            raise forms.ValidationError(_("Passwords don't match"))
        return self.cleaned_data['password2']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta():
        model = User

    def clean_password(self):
        return self.initial['password']
