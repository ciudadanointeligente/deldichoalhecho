from django.views.generic.list import ListView
from ddah_web.models import DDAHInstanceWeb
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class BackendHomeView(ListView):
	model = DDAHInstanceWeb
	template_name = 'home.html'
	context_object_name = 'instances'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(BackendHomeView, self).dispatch(*args, **kwargs)

	def get_queryset(self):
		qs = super(BackendHomeView, self).get_queryset()
		qs = qs.filter(users=self.request.user)
		return qs