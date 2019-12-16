from django.contrib import admin
from . import models

class SubMemberInline(admin.TabularInline):
    model = models.SubMember

admin.site.register(models.Sub)
