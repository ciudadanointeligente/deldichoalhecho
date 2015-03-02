from django.contrib import admin
from promises.models import Category
from promises_instances.models import DDAHCategory

# Register your models here.

admin.site.unregister(Category)


class DDAHCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(DDAHCategory, DDAHCategoryAdmin)
