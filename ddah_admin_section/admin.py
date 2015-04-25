from django.contrib import admin
from ddah_web.models import DDAHInstanceWeb
from ddah_web.admin import DDAHTemplateInline
from ddah_admin_section.forms import DDAHInstanceNonSuperUserForm

# Register your models here.
admin.site.unregister(DDAHInstanceWeb)


@admin.register(DDAHInstanceWeb)
class InstanceAdmin(admin.ModelAdmin):
    form = DDAHInstanceNonSuperUserForm
    inlines = [
        DDAHTemplateInline
    ]
