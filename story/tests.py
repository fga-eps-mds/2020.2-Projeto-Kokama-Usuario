from django.apps import apps
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.test.testcases import SimpleTestCase

from .apps import StoryConfig
from .views import get_search_list, list_story, is_word_in_text, delete_story, add_story_get, add_story_post, add_story


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
        self.assertListEqual(
            filtered_list, [self.story_list[0], self.story_list[1]])

        filtered_list = get_search_list('B1', self.story_list)
        self.assertListEqual(
            filtered_list, [self.story_list[0], self.story_list[2]])

        filtered_list = get_search_list('J', self.story_list)
        self.assertListEqual(filtered_list, [])

        filtered_list = get_search_list('G', [])
        self.assertListEqual(filtered_list, [])

    def test_is_word_in_text(self):
        result = is_word_in_text('banana', 'era uma vez uma banana')
        self.assertEquals(result, True)


class StoryTest(TestCase):

    def setUp(self):
        self.mocked_story_list_url = 'https://6093298ca7e53a00179508bb.mockapi.io/StoryList'

        user = User.objects.create_user(
            'test', 'test@test.com', 'test_password')
        self.request_superuser = self.client.request()
        self.request_superuser.method = 'GET'
        self.request_superuser.user = user

    def test_list_story(self):
        # Is not super user
        response = list_story(self.request_superuser, self.mocked_story_list_url)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, 
                                        target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Search query failed
        self.request_superuser.user.is_superuser = True
        response = list_story(self.request_superuser, self.mocked_story_list_url)
        response.client = Client()


class DeleteTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.mocked_story_list_url = 'https://6093298ca7e53a00179508bb.mockapi.io/StoryList'

        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        self.request_superuser_get = self.factory.get('/')
        self.request_superuser = self.factory.delete('/')
        self.request_superuser_get.method = 'GET'
        self.request_superuser.method = 'DELETE'
        self.request_superuser_get.user = user
        self.request_superuser.user = user

    def test_delete_story(self):
        # Is not super user
        response = delete_story(self.request_superuser, 1, self.mocked_story_list_url)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, 
                                        target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Delete is super user
        self.request_superuser.user.is_superuser = True
        response = delete_story(self.request_superuser, 1, self.mocked_story_list_url)
        self.assertEquals(response.status_code, 302)

        # Delete is super user but wrong url
        response = delete_story(self.request_superuser, 1, 'wrong_url')
        self.assertEquals(response.status_code, 500)


class AddStoryPostGetTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.mocked_story_list_url = 'https://6093298ca7e53a00179508bb.mockapi.io/StoryList'
        self.mocked_story_url = 'https://60a5c020c0c1fd00175f43c0.mockapi.io/EStory'

        user = User.objects.create_user(
            'test', 'test@test.com', 'test_password')
        self.request_user_get = self.factory.get('/')
        self.request_user_post = self.factory.post('/')
        self.request_user_get.method = 'GET'
        self.request_user_post.method = 'POST'
        self.request_user_get.user = user
        self.request_user_post.user = user

    def test_add_story_get(self):
        # If not have id
        response = add_story_get(
            self.request_user_get, '', self.mocked_story_list_url)
        self.assertEquals(response.status_code, 200)

        # Have id but wrong url
        response = add_story_get(self.request_user_get, 1, 'wrong_url')
        self.assertEquals(response.status_code, 500)

    def test_add_story_post(self):
        # Form valid but without id
        response = add_story_post(
            self.request_user_post, '', self.mocked_story_list_url)
        self.assertEquals(response.status_code, 500)

        # Form valid with id
        response = add_story_post(
            self.request_user_post, 1, self.mocked_story_list_url)
        self.assertEquals(response.status_code, 500)


class AddStoryTest(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.mocked_story_list_url = 'https://6093298ca7e53a00179508bb.mockapi.io/StoryList'

        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        self.request_superuser_get = self.factory.get('/')
        self.request_superuser_post = self.factory.post('/')
        self.request_superuser_get.method = 'GET'
        self.request_superuser_post.method = 'POST'
        self.request_superuser_get.user = user
        self.request_superuser_post.user = user
    
    def test_add_story(self):
        # Is not super user
        response = add_story(self.request_superuser_get, 1, self.mocked_story_list_url)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, 
                                        target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Add is super user GET
        self.request_superuser_get.user.is_superuser = True
        response = add_story(self.request_superuser_get, 1, self.mocked_story_list_url)
        self.assertEquals(response.status_code, 500)

        # Add is super user POST
        self.request_superuser_post.user.is_superuser = True
        response = add_story(self.request_superuser_post, 1, self.mocked_story_list_url)
        self.assertEquals(response.status_code, 500)
