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


@admin.register(DDAHInstanceWeb)
class InstanceAdmin(admin.ModelAdmin):
    inlines = [
        DDAHTemplateInline
    ]
