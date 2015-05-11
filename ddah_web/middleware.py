from django.contrib.sites.models import Site
from ddah_web.models import DDAHSiteInstance, DDAHInstanceWeb


class DDAHSiteMiddleware(object):
    def process_request(self, request):
        if hasattr(request, 'instance') and request.instance is not None:
            return
        try:
            record = DDAHSiteInstance.objects.get(site__domain=request.get_host())
            request.instance = record.instance
            if hasattr(request, 'urlconf'):
                del request.urlconf
        except DDAHSiteInstance.DoesNotExist:
            pass

