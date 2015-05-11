from django.template.response import TemplateResponse
from ddah_web.models import DDAHInstanceWeb
from django.views.generic.detail import DetailView
from pystache import Renderer
from django.http import HttpResponse


class MoustacheTemplateResponse(TemplateResponse):
    @property
    def rendered_content(self):
        instance = self.context_data['instance']
        the_bunch = instance.get_as_bunch()
        # this works
        # renderer = Renderer(partials={'h2':"oli {{title}} "})
        partials = {
            "head": instance.template.head,
            "header": instance.template.header,
            "style": instance.template.style,
            "footer": instance.template.footer,
        }
        renderer = Renderer(partials=partials)
        return renderer.render(instance.template.content, the_bunch)


class DDAHInstanceWebView(DetailView):
    response_class = MoustacheTemplateResponse
    model = DDAHInstanceWeb
    context_object_name = 'instance'

    def get_object(self):
        return self.model.objects.get(id=self.request.instance.id)

    def get_slug_field(self):
        return 'label'


class DDAHInstanceWebJSONView(DetailView):
    model = DDAHInstanceWeb
    context_object_name = 'instance'

    def get_object(self):
        return self.model.objects.get(id=self.request.instance.id)

    def get_slug_field(self):
        return 'label'

    def render_to_response(self, context, **response_kwargs):
        response_data = self.object.to_json()
        return HttpResponse(response_data, content_type="application/json")
