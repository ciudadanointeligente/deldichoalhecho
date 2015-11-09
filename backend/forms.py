from django import forms
from promises_instances.csv_loader import DDAHCSVProcessor
from promises_instances.models import DDAHCategory
from promises.models import Promise

class BelongingToInstanceMixin(object):
	def __init__(self, instance, *args, **kwargs):
		self.instance = instance
		return super(BelongingToInstanceMixin, self).__init__(*args, **kwargs)

class CSVUploadForm(BelongingToInstanceMixin, forms.Form):
	csv_file = forms.FileField()

	def upload(self):
		file_ = self.cleaned_data['csv_file']

		processor = DDAHCSVProcessor(file_, self.instance)
		processor.work()


class ColorPickerForm(BelongingToInstanceMixin, forms.Form):
    background_color = forms.CharField()
    second_color = forms.CharField()
    read_more_color = forms.CharField()

    def __init__(self, instance, *args, **kwargs):
        super(ColorPickerForm, self).__init__(instance, *args, **kwargs)
        for key, value in instance.style.items():
            if key in self.fields.keys():
                self.fields[key].initial = value

    def update_colors(self):
        for key, value in self.cleaned_data.items():
            self.instance.style[key] = value
        self.instance.save()
        return self.instance


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = DDAHCategory
        fields = ('name', )

    def __init__(self, ddah_instance, *args, **kwargs):
        self.ddah_instance = ddah_instance
        return super(CategoryCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super(CategoryCreateForm, self).save(commit=False)
        category.instance = self.ddah_instance
        if commit:
            category.save()
        return category


class PromiseCreateForm(forms.ModelForm):
    fulfillment = forms.FloatField()

    def __init__(self, ddah_category, *args, **kwargs):
        self.ddah_category = ddah_category
        super(PromiseCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        promise = super(PromiseCreateForm, self).save(commit=False)
        promise.category = self.ddah_category
        if commit:
            promise.save()
            promise.fulfillment.percentage = self.cleaned_data['fulfillment']
        return promise

    class Meta:
        model = Promise
        fields = ['name','description', 'date', 'ponderator', ]
