from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from sparertid.apps.project.models import Project, SpentTime


class SpentTimeForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        Project.objects.all(),
        to_field_name='alias'
    )

    def clean_project(self):
        user = self.cleaned_data['user']
        project = self.cleaned_data['project']

        if not project.team.filter(pk=user.pk).exists():
            raise forms.ValidationError(_(u"You can't report to this project"))

        return project

    def clean_eta(self):
        now = timezone.localtime(timezone.now())
        eta = timezone.localtime(self.cleaned_data['eta'])

        if eta < now:
            raise forms.ValidationError(_(u'must be in future'))

        return eta

    def clean(self):
        user = self.cleaned_data['user']
        project = self.cleaned_data['project']

        not_ended = SpentTime.objects.filter(
            project=project,
            user=user,
            finished_at__isnull=True
        )
        if not_ended.exists():
            raise forms.ValidationError(
                _(u"You can't create eta because you already have not ended eta")
            )

        return self.cleaned_data

    class Meta:
        model = SpentTime
