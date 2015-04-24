from promises_instances.models import DDAHInstance
from django.db import models
from ddah_web import read_template_as_string
from bunch import Bunch
from promises.models import Promise
import json
import datetime
from ddah_web.templatetags import simple_accomplishment
import markdown


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

    def _bunchify_summary(self, summary):
        return Bunch(
            no_progress=summary.no_progress,
            accomplished=summary.accomplished,
            in_progress=summary.in_progress,
            total=summary.total,
            total_progress=summary.total_progress,
            formated_total_progress="{:10.1f}".format(summary.total_progress),
            accomplished_percentage=summary.accomplished_percentage,
            in_progress_percentage=summary.in_progress_percentage,
            no_progress_percentage=summary.no_progress_percentage,
            )

    def get_as_bunch(self):
        me = Bunch(label=self.label, title=self.title)
        categories = []
        for category in self.categories.all():
            cat_bunch = Bunch(id=category.id, name=category.name, slug=category.slug)
            categories.append(cat_bunch)
            promises = []
            the_promises_from_database = category.promises.all()
            summary = the_promises_from_database.summary()
            cat_bunch.summary = self._bunchify_summary(summary)
            for promise in the_promises_from_database:
                promise_bunch = Bunch(id=promise.id,
                    name=promise.name,
                    description=markdown.markdown(promise.description),
                    date=promise.date)
                promise_bunch.fulfillment = Bunch(percentage=promise.fulfillment.percentage,
                                                  status=promise.fulfillment.status,
                                                  description=markdown.markdown(promise.fulfillment.description),
                                                  simple_accomplishment=simple_accomplishment(promise.fulfillment.percentage)
                                                  )
                verification_documents = []
                for verification_document in promise.verification_documents.all():
                    v_d_bunch = Bunch(id=verification_document.id,
                                      url=verification_document.url,
                                      display_name=verification_document.display_name,
                                      )
                    verification_documents.append(v_d_bunch)
                promise_bunch.verification_documents = verification_documents
                information_sources = []
                for information_source in promise.information_sources.all():
                    i_s_bunch = Bunch(id=information_source.id,
                                      url=information_source.url,
                                      display_name=information_source.display_name,
                                      )
                    information_sources.append(i_s_bunch)
                promise_bunch.information_sources = information_sources

                milestones = []
                for milestone in promise.milestones.all():
                    milestones_bunch = Bunch(id=milestone.id,
                                             date=milestone.date,
                                             description=markdown.markdown(milestone.description),
                                             )
                    milestones.append(milestones_bunch)
                promise_bunch.milestones = milestones

                promises.append(promise_bunch)

            cat_bunch.promises = promises

        me.categories = categories
        summary = Promise.objects.filter(category__in=self.categories.all()).summary()
        me.summary = self._bunchify_summary(summary)
        return me

    def to_json(self):
        bunchified = self.get_as_bunch()
        return json.dumps(bunchified, default=default_json_encoder)

default_template = read_template_as_string('instance_templates/default.html')


class DDAHTemplate(models.Model):
    instance = models.OneToOneField(DDAHInstanceWeb, null=True, related_name="template")
    content = models.TextField(default=default_template)
