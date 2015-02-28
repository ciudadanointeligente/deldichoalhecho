from django.shortcuts import render
from django.views.generic.detail import DetailView
from instances.models import Instance

class InstanceDetailView(DetailView):
	model = Instance

	def get_slug_field(self):
		return 'label'
