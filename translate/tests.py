from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.test.testcases import SimpleTestCase

from .apps import TranslateConfig
from .views import get_word_list, delete_translate

class TranslateConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(TranslateConfig.name, 'translate')
        self.assertEqual(apps.get_app_config('translate').name, 'translate')

#Views.py

class GetTranslateTest(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.mocked_story_list_url = 'https://60a5c020c0c1fd00175f43c0.mockapi.io/EWord'

        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        self.request_superuser_get = self.factory.get('/')
        self.request_superuser_get.method = 'GET'
        self.request_superuser_get.user = user

    def test_get_word_list(self):

        # Is not super user
        response = get_word_list(self.request_superuser_get, self.mocked_story_list_url)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, 
                                        target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Add is super user GET
        self.request_superuser_get.user.is_superuser = True
        response = get_word_list(self.request_superuser_get, self.mocked_story_list_url)
        self.assertEquals(response.status_code, 200)

    def test_delete_translate(self):

        # Is not super user
        response = delete_translate(self.request_superuser_get, 1)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, 
                                        target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Add is super user GET
        self.request_superuser_get.user.is_superuser = True
        response = delete_translate(self.request_superuser_get, 1)
        self.assertEquals(response.status_code, 200)