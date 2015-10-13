from django.forms import ModelForm
from promises_instances.models import DDAHCategory


class CategoryCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.ddah_instance = kwargs.pop('instance')
        super(CategoryCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super(CategoryCreateForm, self).save(commit=False)
        category.instance = self.ddah_instance
        if commit:
            category.save()
        return category

    class Meta:
        model = DDAHCategory
        fields = ['name', ]

