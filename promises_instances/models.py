from django.db import models
from promises.models import Category
from instances.models import Instance

# Create your models here.
class DDAHCategory(Category):
	instance = models.ForeignKey(Instance, related_name='categories')
