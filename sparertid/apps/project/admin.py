from django.contrib import admin

from .models import Project, Membership, SpentTime

admin.site.register(Project)
admin.site.register(Membership)
admin.site.register(SpentTime)