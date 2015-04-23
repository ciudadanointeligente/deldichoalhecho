from promises_instances.models import DDAHInstance
from django.db import models
from ddah_web import read_template_as_string


class DDAHInstanceWeb(DDAHInstance):
    def save(self, *args, **kwargs):
        creating = self.id is None
        super(DDAHInstanceWeb, self).save(*args, **kwargs)
        if creating:
            DDAHTemplate.objects.create(instance=self)


default_template = read_template_as_string('instance_templates/default.html')


class DDAHTemplate(models.Model):
    instance = models.OneToOneField(DDAHInstanceWeb, null=True, related_name="template")
    content = models.TextField(default=default_template)
