from django.db import models
from promises.models import Category, Promise
from instances.models import Instance


class DDAHInstance(Instance):
    pass


class DDAHCategory(Category):
    instance = models.ForeignKey(DDAHInstance, related_name='categories')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order', )


class DDAHPromise(Promise):
    instance = models.ForeignKey(DDAHInstance, related_name='promises')

    def save(self, *args, **kwargs):
        if self.category is not None:
            self.instance = self.category.instance
        return super(DDAHPromise, self).save()
