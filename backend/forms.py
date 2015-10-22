from django import forms
from promises_instances.csv_loader import DDAHCSVProcessor

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
