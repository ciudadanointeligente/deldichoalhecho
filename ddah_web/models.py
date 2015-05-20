from promises_instances.models import DDAHInstance
from django.db import models
from ddah_web import read_template_as_string
from bunch import Bunch
from promises.models import Promise
import json
import datetime
from ddah_web.templatetags import simple_accomplishment
import markdown
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse
from picklefield.fields import PickledObjectField
from django.contrib.flatpages.models import FlatPage
from urlparse import urljoin


def default_json_encoder(o):
    if isinstance(0, datetime.date) or isinstance(0, datetime.datetime):
        return o.isoformat()


# This could easily be a proxy model
# I'm waiting until the end of the day to see what happens
class DDAHInstanceWeb(DDAHInstance):
    contact = models.EmailField(max_length=254, null=True, blank=True)
    style = PickledObjectField(default={})
    social_networks = PickledObjectField(default={})

    def save(self, *args, **kwargs):
        creating = self.id is None
        if creating:
            default_style = getattr(settings, 'DEFAULT_STYLE', {})
            if not self.style and default_style:
                self.style = default_style
            default_social_networks = getattr(settings, 'DEFAULT_SOCIAL_NETWORKS', {})
            if not self.social_networks and default_social_networks:
                self.social_networks = default_social_networks
        super(DDAHInstanceWeb, self).save(*args, **kwargs)
        if creating:
            DDAHTemplate.objects.create(instance=self)
            if not self.style and default_style:
                self.style = default_style

    @property
    def url(self):
        return '%s.%s' % (self.label, settings.BASE_HOST)

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

    def get_flatpages(self):
        result = []
        for flatpage in self.ddahflatpage_set.all():
            bunch = Bunch(title=flatpage.title, url=flatpage.get_absolute_url())
            result.append(bunch)

        return result

    def get_as_bunch(self):
        home_url = reverse('instance_home')
        home_url = '%s%s' % (self.url, home_url)
        me = Bunch(label=self.label,
                   title=self.title,
                   description=self.description,
                   url=home_url,
                   contact=self.contact,)
        me.flatpages = self.get_flatpages()
        style = getattr(settings, 'DEFAULT_STYLE', {})
        style.update(self.style)
        me.style = Bunch.fromDict(style)
        social_networks = getattr(settings, 'DEFAULT_SOCIAL_NETWORKS', {})
        social_networks.update(self.social_networks)
        me.social_networks = Bunch.fromDict(social_networks)
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

    def get_absolute_url(self):
        sites = Site.objects.filter(ddahsiteinstance__instance=self)
        if sites:
            return "http://%s" % (sites.first().domain)
        return super(DDAHInstanceWeb, self).get_absolute_url()

default_template = read_template_as_string('instance_templates/default.html')
default_template_flat_page = read_template_as_string('instance_templates/default_flat_page.html')
default_template_head = read_template_as_string('instance_templates/partials/head.html')
default_template_header = read_template_as_string('instance_templates/partials/header.html')
default_template_style = read_template_as_string('instance_templates/partials/style.html')
default_template_footer = read_template_as_string('instance_templates/partials/footer.html')


class DDAHTemplate(models.Model):
    instance = models.OneToOneField(DDAHInstanceWeb, null=True, related_name="template")
    content = models.TextField(default=default_template)
    flat_page_content = models.TextField(default=default_template_flat_page)
    head = models.TextField(default=default_template_head)
    header = models.TextField(default=default_template_header)
    style = models.TextField(default=default_template_style)
    footer = models.TextField(default=default_template_footer)


class DDAHSiteInstance(models.Model):
    instance = models.OneToOneField(DDAHInstanceWeb)
    site = models.OneToOneField(Site)

    def __unicode__(self):
        dicti = {
            'domain': self.site.domain,
            'instance_title': self.instance.title
        }
        return u"{domain} redirects to {instance_title}".format(**dicti)


class DdahFlatPage(FlatPage):
    instance = models.ForeignKey(DDAHInstanceWeb)

    def get_absolute_url(self):
        url = reverse('flat_page', kwargs={'url': self.url})
        return urljoin(self.instance.get_absolute_url(), url)
