from django.shortcuts import render
from django.views.generic.detail import DetailView
from instances.models import Instance
from promises_instances.models import DDAHCategory
from django.db.models import Avg


class InstanceDetailView(DetailView):
    model = Instance

    def get_slug_field(self):
        return 'label'

    def order_categories(self, categories_queryset):
        queryset = categories_queryset.annotate(percentage = Avg('promises__fulfillment__percentage'))
        ordered_categories = queryset.order_by('-percentage')
        return ordered_categories

    def get_context_data(self, **kwargs):
        context = super(InstanceDetailView, self).get_context_data(**kwargs)
        categories = DDAHCategory.objects.filter(instance=self.object)
        categories = self.order_categories(categories)
        context['categories'] = categories
        return context
