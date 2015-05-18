from django.contrib import admin
from ddah_web.models import DDAHInstanceWeb, DDAHTemplate, DDAHSiteInstance, DdahFlatPage
from ddah_web.admin import DDAHTemplateInline
from ddah_admin_section.forms import DDAHInstanceNonSuperUserForm, DDAHInstanceForm
from promises_instances.models import DDAHCategory, DDAHInstance
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from promises.models import Promise, Category
from promises.admin import PromiseAdmin
from django.contrib.flatpages.models import FlatPage
from django import forms
# Register your models here.
admin.site.unregister(DDAHInstanceWeb)
admin.site.unregister(DDAHCategory)
admin.site.unregister(Promise)
admin.site.unregister(FlatPage)


@admin.register(DdahFlatPage)
class DdahFlatPageAdmin(admin.ModelAdmin):
    exclude = ('sites', "template_name", "registration_required", )

@admin.register(DDAHTemplate)
class DDAHTemplateAdmin(admin.ModelAdmin):
    pass


class DDAHCategoryInline(SortableInlineAdminMixin, admin.TabularInline):
    model = DDAHCategory
    extra = 0


@admin.register(DDAHInstanceWeb)
class InstanceAdmin(admin.ModelAdmin):
    form = DDAHInstanceForm
    inlines = [
        DDAHTemplateInline,
        DDAHCategoryInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(InstanceAdmin, self).get_form(request, obj, **kwargs)
        return DDAHInstanceNonSuperUserForm

    def get_queryset(self, request):
        qs = super(InstanceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users=request.user)


class DDAHCategoryForm(forms.ModelForm):
    instance = forms.ModelChoiceField(queryset=DDAHInstanceWeb.objects.none())

    class Meta:
        model = DDAHCategory
        fields = ('instance', 'name', )

    def __init__(self, *args, **kwargs):
        result = super(DDAHCategoryForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            user = kwargs['initial']['user']
            self.fields['instance'].queryset = DDAHInstanceWeb.objects.filter(users=user)
        else:
            self.fields['instance'].queryset = DDAHInstanceWeb.objects.all()
        return result


@admin.register(DDAHCategory)
class DDAHCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(DDAHCategoryAdmin, self).get_form(request, obj, **kwargs)
        return DDAHCategoryForm

    def get_changeform_initial_data(self, request):
        initial = super(DDAHCategoryAdmin, self).get_changeform_initial_data(request)
        initial['user'] = request.user
        return initial

    def get_queryset(self, request):
        qs = super(DDAHCategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instance__users=request.user)


def get_categories_by_user(user):
    ddahinstances = DDAHInstance.objects.filter(id__in=[i.id for i in user.instances.all()])
    ddahcategories = DDAHCategory.objects.filter(instance__in=ddahinstances)
    categories = Category.objects.filter(id__in=[i.id for i in ddahcategories.all()])
    return categories


class DDAHPromiseAdminForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=DDAHCategory.objects.none())

    class Meta:
        model = Promise
        exclude = ()

    def __init__(self, *args, **kwargs):
        result = super(DDAHPromiseAdminForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            user = kwargs['initial']['user']
            self.fields['category'].queryset = DDAHCategory.objects.filter(instance__users=user)
        else:
            self.fields['category'].queryset = DDAHCategory.objects.all()
        return result


@admin.register(Promise)
class DDAHPromiseAdmin(PromiseAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(DDAHPromiseAdmin, self).get_form(request, obj, **kwargs)
        return DDAHPromiseAdminForm

    def get_changeform_initial_data(self, request):
        initial = super(DDAHPromiseAdmin, self).get_changeform_initial_data(request)
        initial['user'] = request.user
        return initial

    def get_queryset(self, request):
        qs = super(DDAHPromiseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(category__in=get_categories_by_user(request.user))

@admin.register(DDAHSiteInstance)
class DDAHSiteInstanceAdmin(admin.ModelAdmin):
    pass
