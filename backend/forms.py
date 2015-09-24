from django import forms
from promises_instances.csv_loader import DDAHCSVProcessor


class CSVUploadForm(forms.Form):
	csv_file = forms.FileField()

	def __init__(self, instance, *args, **kwargs):
		self.instance = instance
		return super(CSVUploadForm, self).__init__(*args, **kwargs)

	def upload(self):
		file_ = self.cleaned_data['csv_file']

		processor = DDAHCSVProcessor(file_, self.instance)
		processor.work()
