from django.test import TestCase
from django.apps import apps
from .apps import TranslateConfig

class TranslateConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(TranslateConfig.name, 'translate')
        self.assertEqual(apps.get_app_config('translate').name, 'translate')

