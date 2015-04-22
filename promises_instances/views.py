from django.views.generic.detail import DetailView
from promises_instances.models import DDAHInstance


class InstanceDetailView(DetailView):
    model = DDAHInstance
    context_object_name = 'instance'

    def get_slug_field(self):
        return 'label'

    def get_context_data(self, **kwargs):
        context = super(InstanceDetailView, self).get_context_data(**kwargs)
        context['categories'] = self.object.categories.all()
        return context
