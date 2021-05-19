from django.test import TestCase, RequestFactory
from django.apps import apps
from django.contrib.auth.models import User
from django.test.client import Client
from django.test.testcases import SimpleTestCase
from requests.models import Response
from .apps import AdministrationConfig
from .views import admin_register, login
from .forms import save

class AdministrationConfigTest(TestCase):

    def test_apps(self):
        self.assertEqual(AdministrationConfig.name, 'administration')
        self.assertEqual(apps.get_app_config('administration').name, 'administration')


# Views.py

class AdminRegisterTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        
        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        self.request_superuser = self.factory.get('/')
        self.request_superuser.user = user

        
        self.request_is_post = self.factory.post('/')
        self.request_is_post.user = user

        self.request_is_get = self.factory.get('/')
        self.request_is_get.user = user

        data = {
            'username': 'qweqwrfdxhasdg',
            'password1': 'cvbcvn1sadffdghfjdjfk',
            'password2': 'cvbcvn1sadffdghfjdjfk',
        }

        self.request_form_is_valid = self.factory.post('/', data)
        self.request_form_is_valid.user = user

    def test_admin_register(self):

        # Not superuser
        response = admin_register(self.request_superuser)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=False)

        # Post
        ## Form not valid
        self.request_is_post.user.is_superuser = True
        response = admin_register(self.request_is_post)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        ## Form valid
        response = admin_register(self.request_form_is_valid)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=False)

        # Get
        response = admin_register(self.request_is_get)
        self.assertEqual(response.status_code, 200)


class LoginTest(TestCase):

    def setUp(self):
        
        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        user.is_superuser = True
        self.request_get = self.client.request()
        self.request_get.method = 'GET'
        self.request_get.user = user
        
        data = {
            'username': 'test',
            'password': 'test_password',
        }

        self.factory = RequestFactory()
        self.request_form_is_valid = self.factory.post('/', data)

    def test_login(self):

        # Get
        response = login(self.request_get)
        response.client = Client()
        SimpleTestCase.assertRedirects(self, response=response, expected_url='/traducao/lista_de_palavras/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=False)

        ## Form valid
        response = login(self.request_form_is_valid)
        response.client = Client()
        self.assertEqual(response.status_code, 200)


# Forms.py

class UserCreationFormTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('test', 'test@test.com', 'test_password')
        Save = save.object.create('email')

    def test_save(self):
        response = email(self.save('email'))
        self.assertEquals(response.status_code, 200)