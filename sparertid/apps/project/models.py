from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    name = models.CharField(
        _('Project name'), max_length=50,
        unique=True
    )
    alias = models.CharField(
        _('Alias'), max_length=10,
        unique=True
    )
    team = models.ManyToManyField(
        get_user_model(),
        through='Membership',
        verbose_name=_('Team')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='teams',
        verbose_name=_('Project')
    )
    user = models.ForeignKey(
        get_user_model(),
        related_name='teams',
        verbose_name=_('User')
    )
    date_joined = models.DateField(_('Date joined'))


class SpentTime(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='spent_time',
        verbose_name=_('User')
    )
    project = models.ForeignKey(
        Project,
        related_name='spent_time',
        verbose_name=_('Project')
    )
    task = models.CharField(_('Task'), max_length=300)
    started_at = models.DateTimeField(_('Started at'))
    finished_at = models.DateTimeField(_('Finished at'), null=True, blank=True)
    eta = models.DateTimeField(_('Estimated Arrival Times'))
    spent_time = models.FloatField(_('Spent time'), null=True, blank=True)

    def finish(self):
        self.finished_at = timezone.localtime(timezone.now())
        if self.finished_at > self.eta:
            self.finished_at = self.eta
        self.spent_time = (self.finished_at - self.started_at).total_seconds()
        self.save()
