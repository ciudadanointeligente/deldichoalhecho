from django.contrib import admin
from promises_instances.models import Instance
# Register your models here.
admin.site.unregister(Instance)

from ddah_web.models import DDAHInstanceWeb, DDAHTemplate


class DDAHTemplateInline(admin.TabularInline):
    model = DDAHTemplate


@admin.register(DDAHInstanceWeb)
class InstanceAdmin(admin.ModelAdmin):
    inlines = [
        DDAHTemplateInline
    ]
