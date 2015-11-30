from django.views.generic.list import ListView
from ddah_web.models import DDAHInstanceWeb, DDAHTemplate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from backend.forms import CSVUploadForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from promises_instances.models import DDAHCategory
from .forms import ColorPickerForm, CategoryCreateForm, PromiseCreateForm, PromiseUpdateForm
from promises.models import Promise


class BackendBase(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(BackendBase, self).dispatch(*args, **kwargs)


class InstanceBase(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		# if self.request.user not in
		self.ddah_instance = self.get_object()
		if self.request.user not in self.ddah_instance.users.all():
			return HttpResponse('Unauthorized', status=401)
		return super(InstanceBase, self).dispatch(*args, **kwargs)


class BackendHomeView(ListView, BackendBase):
	model = DDAHInstanceWeb
	template_name = 'home.html'
	context_object_name = 'instances'

	def get_queryset(self):
		qs = super(BackendHomeView, self).get_queryset()
		qs = qs.filter(users=self.request.user)
		return qs


class InstanceDetailView(DetailView, InstanceBase):
	model = DDAHInstanceWeb
	template_name = 'instance_detail.html'
	context_object_name = 'instance'
	slug_field = 'label'


class StyleView(InstanceBase, FormView):
    template_name = 'style_color_picker.html'
    form_class = ColorPickerForm

    def get_object(self):
        self.instance =  get_object_or_404(DDAHInstanceWeb, label=self.kwargs['slug'])
        return self.instance

    def get_form_kwargs(self):
		kwargs = super(StyleView, self).get_form_kwargs()
		kwargs.update({'instance': self.instance})
		return kwargs

    def get_success_url(self):
        url = reverse('backend:instance_style', kwargs={'slug': self.instance.label})
        return url

    def form_valid(self, form):
        form.update_colors()
        return super(StyleView, self).form_valid(form)



class CSVUploadView(FormView, InstanceBase):
	template_name = 'csv_upload.html'
	form_class = CSVUploadForm

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		self.instance = get_object_or_404(DDAHInstanceWeb, label=self.kwargs['slug'])
		if self.request.user not in self.instance.users.all():
			return HttpResponse('Unauthorized', status=401)
		return super(InstanceBase, self).dispatch(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CSVUploadView, self).get_form_kwargs()
		kwargs.update({'instance': self.instance})
		return kwargs

	def form_valid(self, form):
		form.upload()
		return super(CSVUploadView, self).form_valid(form)

	def get_success_url(self):
		return reverse('backend:instance', kwargs={'slug': self.instance.label})


class PromiseCreateView(CreateView):
    form_class = PromiseCreateForm
    model = Promise

    def get_form_kwargs(self):
        kwargs = super(PromiseCreateView, self).get_form_kwargs()
        self.category = DDAHCategory.objects.get(id=self.kwargs['category_id'])
        kwargs.update({'ddah_category': self.category})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PromiseCreateView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_success_url(self):
        return reverse('backend:instance', kwargs={'slug': self.category.instance.label})


class PromiseUpdateView(UpdateView):
    model = Promise
    form_class = PromiseUpdateForm
    template_name = "promises/promise_update.html"

    def get_success_url(self):
        ddah_category = DDAHCategory.objects.get(id=self.object.category.id)
        return reverse('backend:instance', kwargs={'slug': ddah_category.instance.label})

class CategoryCreateView(CreateView, InstanceBase):
    form_class = CategoryCreateForm
    model = DDAHCategory
    template_name = 'category_create.html'

    def get_object(self):
        instance =  get_object_or_404(DDAHInstanceWeb, label=self.kwargs['slug'])
        return instance

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['instance'] = self.ddah_instance
        return context

    def get_form_kwargs(self):
        kwargs = super(CategoryCreateView, self).get_form_kwargs()
        kwargs.update({'ddah_instance': self.ddah_instance})
        return kwargs

    def get_success_url(self):
        return reverse('backend:instance', kwargs={'slug': self.ddah_instance.label})


class CreateInstanceView(CreateView):
    model = DDAHInstanceWeb
    fields = ('title', 'label', )
    template_name = 'instances/create.html'

    def form_valid(self, form):
        self.ddah_instance = form.save()
        self.ddah_instance.users.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('backend:instance', kwargs={'slug': self.ddah_instance.label})

class TemplateUpdateView(UpdateView):
    model = DDAHTemplate
    fields = ('content', 'flat_page_content', 'head', 'header', 'style', 'footer', )
    template_name = 'instances/update_template.html'
    slug_field = 'instance__label'

    def get_success_url(self):
        return reverse('backend:update_template', kwargs={'slug': self.object.instance.label})


