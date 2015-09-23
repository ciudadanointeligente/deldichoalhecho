from promises.csv_loader import CsvProcessor
from promises_instances.models import DDAHCategory, DDAHPromise

class DDAHCSVProcessor(CsvProcessor):
    def __init__(self, file_, instance, **kwargs):
        self.instance = instance
        cat_qs = DDAHCategory.objects.filter(instance=self.instance)
        promise_qs = DDAHPromise.objects.filter(instance=self.instance)
        kwargs['category_qs'] = cat_qs
        kwargs['promise_qs'] = promise_qs
        kwargs['instance'] = self.instance
        super(DDAHCSVProcessor, self).__init__(file_, **kwargs)
