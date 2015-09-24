from django.views.generic.list import ListView
from ddah_web.models import DDAHInstanceWeb
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.http import HttpResponse
from django.views.generic.edit import FormView
from backend.forms import CSVUploadForm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse


class BackendBase(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(BackendBase, self).dispatch(*args, **kwargs)


class InstanceBase(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		# if self.request.user not in 
		instance = self.get_object()
		if self.request.user not in instance.users.all():
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
