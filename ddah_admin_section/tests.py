from django.test import TestCase
from ddah_admin_section.forms import DDAHInstanceNonSuperUserForm


class DDAHInstanceNonSuperUserFormTestCase(TestCase):
    fixtures = ['100dias.json']

    def setUp(self):
        pass

    def test_form_instanciate(self):
        data = {
            'label': 'bici',
            'title': 'la bicicleta'
        }
        form = DDAHInstanceNonSuperUserForm(data=data)
        self.assertNotIn('user', form.fields)
        self.assertNotIn('created_by', form.fields)
