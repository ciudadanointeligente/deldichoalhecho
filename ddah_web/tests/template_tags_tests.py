from django.test import TestCase
from ddah_web.templatetags import simple_accomplishment, all_template_tags
# Ok so in order for this templatetags to work with
# moustache they have to be python functions


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        pass

    def test_simple_accomplishment_is_in_the_dictionary_of_template_tags(self):
        self.assertEquals(all_template_tags['simple_accomplishment'], simple_accomplishment)

    def test_simple_accomplishement(self):

        self.assertEquals(simple_accomplishment(0), 'not-accomplished')
        self.assertEquals(simple_accomplishment(45), 'half-accomplished')
        self.assertEquals(simple_accomplishment(100), 'accomplished')

        self.assertFalse(simple_accomplishment('a'))
