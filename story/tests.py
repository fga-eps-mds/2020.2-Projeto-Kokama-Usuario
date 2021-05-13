from django.test import TestCase
from django.apps import apps
from .apps import StoryConfig

class StoryConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(StoryConfig.name, 'story')
        self.assertEqual(apps.get_app_config('story').name, 'story')

