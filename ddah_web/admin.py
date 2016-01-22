from django.contrib import admin
from promises_instances.models import Instance
from django import forms
from ddah_web.models import DDAHInstanceWeb, DDAHTemplate
from django_ace import AceWidget
# Register your models here.


admin.site.unregister(Instance)


class TemplateForm(forms.ModelForm):
    class Meta:
        model = DDAHTemplate
        widgets = {
            "content": AceWidget(mode='html'),
            "head": AceWidget(mode='html'),
            "header": AceWidget(mode='html'),
            "footer": AceWidget(mode='html'),
            "style": AceWidget(mode='html'),
            "flat_page_content": AceWidget(mode='html'),
        }
        fields = ('content', "head", "header", "footer", "style", "flat_page_content", )


class DDAHTemplateInline(admin.TabularInline):
    model = DDAHTemplate
    form = TemplateForm

    def get_extra(self, request, obj=None, **kwargs):
        return 0


@admin.register(DDAHInstanceWeb)
class InstanceAdmin(admin.ModelAdmin):
    inlines = [
        DDAHTemplateInline
    ]
