from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.test.testcases import SimpleTestCase

from .apps import StoryConfig
from .views import get_search_list, list_story, is_word_in_text


class StoryConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(StoryConfig.name, 'story')
        self.assertEqual(apps.get_app_config('story').name, 'story')


# Views.py

class GetSearchListTest(TestCase):

    def setUp(self):

        self.story_list = [
            {
                'title_portuguese': 'titulo portugues A1',
                'text_portuguese': 'text portugues C1',
                'title_kokama': 'titulo kokama B1',
                'text_kokama': 'text kokama C1'
            },
            {
                'title_portuguese': 'titulo portugues A1',
                'text_portuguese': 'text portugues D1',
                'title_kokama': 'titulo kokama A2',
                'text_kokama': 'text kokama D1'
            },
            {
                'title_portuguese': 'titulo portugues B1',
                'text_portuguese': 'text portugues C2',
                'title_kokama': 'titulo kokama B1',
                'text_kokama': 'text kokama C2'
            },
            {
                'title_portuguese': 'titulo portugues D1',
                'text_portuguese': 'banana',
                'title_kokama': 'titulo kokama D1',
                'text_kokama': 'panara'
            },
        ]

    def test_get_search_list(self):
        
        filtered_list = get_search_list('A1', self.story_list)
        self.assertListEqual(filtered_list, [ self.story_list[0], self.story_list[1] ])

        filtered_list = get_search_list('B1', self.story_list)
        self.assertListEqual(filtered_list, [ self.story_list[0], self.story_list[2] ])

        filtered_list = get_search_list('J', self.story_list)
        self.assertListEqual(filtered_list, [])

        filtered_list = get_search_list('G', [])
        self.assertListEqual(filtered_list, [])

    def test_is_word_in_text(self):
        result = is_word_in_text('banana','era uma vez uma banana')
        self.assertEquals(result, True)

class StoryTest(TestCase):

    def setUp(self):
        self.mocked_story_list_url = 'https://6093298ca7e53a00179508bb.mockapi.io/StoryList'

        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        self.request_superuser = self.client.request()
        self.request_superuser.method = 'GET'
        self.request_superuser.user = user
    
    def test_list_story(self):
        # Is not super user
        response = list_story(self.request_superuser, self.mocked_story_list_url)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Search query failed
        self.request_superuser.user.is_superuser = True
        response = list_story(self.request_superuser, self.mocked_story_list_url)
        response.client = Client()
    