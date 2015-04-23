from django.template.response import TemplateResponse
from ddah_web.models import DDAHInstanceWeb
from django.views.generic.detail import DetailView


class MoustacheTemplateThing(TemplateResponse):
    @property
    def rendered_content(self):
        instance = self.context_data['instance']
        the_json = instance.to_json()
        return ''


class DDAHInstanceWebView(DetailView):
    response_class = MoustacheTemplateThing
    model = DDAHInstanceWeb
    context_object_name = 'instance'

    def get_slug_field(self):
        return 'label'
