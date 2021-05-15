from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.test.testcases import SimpleTestCase

from .apps import StoryConfig
from .views import get_search_list, list_story


class StoryConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(StoryConfig.name, 'story')
        self.assertEqual(apps.get_app_config('story').name, 'story')


# Views

class GetSearchListTest(TestCase):

    def setUp(self):

        self.story_list = [
            {
                'title': 'titulo A1',
                'text': 'text C1'
            },
            {
                'title': 'titulo A2',
                'text': 'text D1'
            },
            {
                'title': 'titulo B1',
                'text': 'text C2'
            },
        ]

    def test_get_search_list(self):
        
        filtered_list = get_search_list('A', self.story_list)
        self.assertListEqual(filtered_list, [ self.story_list[0], self.story_list[1] ])

        filtered_list = get_search_list('C', self.story_list)
        self.assertListEqual(filtered_list, [ self.story_list[0], self.story_list[2] ])

        filtered_list = get_search_list('J', self.story_list)
        self.assertListEqual(filtered_list, [])

        filtered_list = get_search_list('G', [])
        self.assertListEqual(filtered_list, [])


class StoryTest(TestCase):

    def setUp(self):
        self.mocked_story_list_url = 'https://6093298ca7e53a00179508bb.mockapi.io/StoryList'

        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        self.request_superuser = self.client.request()
        self.request_superuser.method = 'GET'
        self.request_superuser.user = user


    
    def test_list_story(self):
        response = list_story(self.request_superuser, self.mocked_story_list_url)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        self.request_superuser.user.is_superuser = True
        response = list_story(self.request_superuser, self.mocked_story_list_url)
        response.client = Client()
    