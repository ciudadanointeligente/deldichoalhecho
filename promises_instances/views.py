from django.shortcuts import render
from django.views.generic.detail import DetailView
from instances.models import Instance
from promises_instances.models import DDAHCategory

class InstanceDetailView(DetailView):
    model = Instance

    def get_slug_field(self):
        return 'label'

    def get_context_data(self, **kwargs):
        context = super(InstanceDetailView, self).get_context_data(**kwargs)
        categories = DDAHCategory.objects.filter(instance=self.object)
        context['categories'] = categories
        return context
