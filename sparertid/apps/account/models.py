import pytz
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):

    GENDER_MALE, GENDER_FEMALE = 'M', 'F'
    GENDER = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
    )

    email = models.EmailField(
        _('Email'),
        max_length=100,
        unique=True
    )

    jid = models.EmailField(
        _('Jabber ID'),
        max_length=100,
        unique=True
    )

    timezone = models.CharField(
        _(u'Time Zone'),
        max_length=40,
        choices=zip(*[pytz.common_timezones]*2)
    )

    first_name = models.CharField(
        _('First name'), max_length=50,
        blank=True, null=True
    )

    last_name = models.CharField(
        _('Last name'), max_length=50,
        blank=True, null=True
    )

    gender = models.CharField(
        _('Gender'), max_length=1,
        blank=True, null=True, choices=GENDER
    )

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['jid',]
    objects = UserManager()

    def get_username(self):
        return self.email.split('@')[0]

    def get_short_name(self):
        return self.get_username()
