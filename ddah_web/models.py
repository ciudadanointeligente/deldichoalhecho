from promises_instances.models import DDAHInstance
from django.db import models
from ddah_web import read_template_as_string
from bunch import Bunch
from promises.models import Promise
import json
import datetime


def default_json_encoder(o):
    if isinstance(0, datetime.date) or isinstance(0, datetime.datetime):
        return o.isoformat()


# This could easily be a proxy model
# I'm waiting until the end of the day to see what happens
class DDAHInstanceWeb(DDAHInstance):
    def save(self, *args, **kwargs):
        creating = self.id is None
        super(DDAHInstanceWeb, self).save(*args, **kwargs)
        if creating:
            DDAHTemplate.objects.create(instance=self)

    def get_as_bunch(self):
        me = Bunch(label=self.label, title=self.title)
        categories = Bunch()
        for category in self.categories.all():
            cat_bunch = Bunch(id=category.id, name=category.name, slug=category.slug)
            categories[category.id] = cat_bunch
            promises = Bunch()
            for promise in category.promises.all():
                promise_bunch = Bunch(id=promise.id,
                    name=promise.name,
                    description=promise.description,
                    date=promise.date)
                promise_bunch.fulfillment = Bunch(percentage=promise.fulfillment.percentage,
                                                  status=promise.fulfillment.status,
                                                  description=promise.fulfillment.description
                                                  )
                verification_documents = Bunch()
                for verification_document in promise.verification_documents.all():
                    v_d_bunch = Bunch(id=verification_document.id,
                                      url=verification_document.url,
                                      display_name=verification_document.display_name,
                                      )
                    verification_documents[verification_document.id] = v_d_bunch
                promise_bunch.verification_documents = verification_documents
                information_sources = Bunch()
                for information_source in promise.information_sources.all():
                    i_s_bunch = Bunch(id=information_source.id,
                                      url=information_source.url,
                                      display_name=information_source.display_name,
                                      )
                    information_sources[information_source.id] = i_s_bunch
                promise_bunch.information_sources = information_sources

                milestones = Bunch()
                for milestone in promise.milestones.all():
                    milestones_bunch = Bunch(id=milestone.id,
                                             date=milestone.date,
                                             description=milestone.description,
                                             )
                    milestones[milestone.id] = milestones_bunch
                promise_bunch.milestones = milestones

                promises[promise.id] = promise_bunch

            cat_bunch.promises = promises

        me.categories = categories
        summary = Promise.objects.filter(category__in=self.categories.all()).summary()
        me.summary = Bunch(
            no_progress=summary.no_progress,
            accomplished=summary.accomplished,
            in_progress=summary.in_progress,
            total=summary.total,
            total_progress=summary.total_progress,
            accomplished_percentage=summary.accomplished_percentage,
            in_progress_percentage=summary.in_progress_percentage,
            no_progress_percentage=summary.no_progress_percentage,
            )
        return me

    def to_json(self):
        bunchified = self.get_as_bunch()
        return json.dumps(bunchified, default=default_json_encoder)

default_template = read_template_as_string('instance_templates/default.html')


class DDAHTemplate(models.Model):
    instance = models.OneToOneField(DDAHInstanceWeb, null=True, related_name="template")
    content = models.TextField(default=default_template)
