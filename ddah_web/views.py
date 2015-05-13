from django.template.response import TemplateResponse
from ddah_web.models import DDAHInstanceWeb, DdahFlatPage
from django.views.generic.detail import DetailView
from pystache import Renderer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import markdown


class MoustacheTemplateResponseBase(TemplateResponse):
    def __init__(self, request, template, context=None, content_type=None, status=None,
                 charset=None, using=None, context_object_name='instance',
                 ddah_template=None
                 ):
        super(MoustacheTemplateResponseBase, self).__init__(request,
                                                            template,
                                                            context,
                                                            content_type,
                                                            status,
                                                            charset,
                                                            using
                                                            )
        self.context_object_name = context_object_name

    def get_instance(self):
        return self.context_data[self.context_object_name]

    def get_the_data(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_template(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_partials(self):
        template = self.get_template()
        return {
            "head": template.head,
            "header": template.header,
            "style": template.style,
            "footer": template.footer,
        }

    def get_content(self):
        return self.get_template().content

    @property
    def rendered_content(self):
        renderer = Renderer(partials=self.get_partials())
        return renderer.render(self.get_content(), self.get_the_data())


class MoustacheTemplateResponse(MoustacheTemplateResponseBase):
    def get_the_data(self):
        instance = self.get_instance()
        return instance.get_as_bunch()

    def get_template(self):
        return self.get_instance().template


class MoustacheFlatPageTemplateResponse(MoustacheTemplateResponseBase):
    def get_content(self):
        return self.get_template().flat_page_content

    def get_the_data(self):
        flatpage = self.get_instance()
        data = flatpage.instance.get_as_bunch()
        del data.summary
        del data.categories
        data.page_title = flatpage.title
        data.page_content = markdown.markdown(flatpage.content)
        data.enable_comments = flatpage.enable_comments
        return data

    def get_template(self):
        return self.get_instance().instance.template


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


class FlatPageView(DetailView):
    model = DdahFlatPage
    response_class = MoustacheFlatPageTemplateResponse
    context_object_name = 'instance'

    def get_object(self):
        return get_object_or_404(DdahFlatPage, url=self.kwargs['url'], instance__id=self.request.instance.id)
