from django.db import models
from promises.models import Category
from instances.models import Instance


class DDAHInstance(Instance):
    pass


class DDAHCategory(Category):
    instance = models.ForeignKey(DDAHInstance, related_name='categories')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order', )

