from django.contrib import admin
from promises_instances.models import Instance
from django import forms
# Register your models here.
admin.site.unregister(Instance)

from ddah_web.models import DDAHInstanceWeb, DDAHTemplate
from django_ace import AceWidget


class TemplateForm(forms.ModelForm):
    class Meta:
        model = DDAHTemplate
        widgets = {
            "content": AceWidget(mode='html'),
        }
        fields = ('content', )


class DDAHTemplateInline(admin.TabularInline):
    model = DDAHTemplate
    form = TemplateForm

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return 0


@admin.register(DDAHInstanceWeb)
class InstanceAdmin(admin.ModelAdmin):
    inlines = [
        DDAHTemplateInline
    ]
