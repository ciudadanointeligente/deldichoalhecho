from django.views.generic.detail import DetailView
from promises_instances.models import DDAHInstance
from promises.models import Promise


class InstanceDetailView(DetailView):
    model = DDAHInstance
    context_object_name = 'instance'

    def get_context_data(self, **kwargs):
        context = super(InstanceDetailView, self).get_context_data(**kwargs)
        context['categories'] = self.object.categories.all()
        context['summary'] = Promise.objects.filter(category__in=self.object.categories.all()).summary()
        return context
