from django.template.response import TemplateResponse
from ddah_web.models import DDAHInstanceWeb
from django.views.generic.detail import DetailView
import pystache


class MoustacheTemplateResponse(TemplateResponse):
    @property
    def rendered_content(self):
        instance = self.context_data['instance']
        the_bunch = instance.get_as_bunch()
        return pystache.render(instance.template.content, the_bunch)


class DDAHInstanceWebView(DetailView):
    response_class = MoustacheTemplateResponse
    model = DDAHInstanceWeb
    context_object_name = 'instance'

    def get_slug_field(self):
        return 'label'
