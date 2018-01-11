import json

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from urllib.parse import urlencode


class RegistrationTestCase(TestCase):
    ACCOUNT_INFO = {
        'email': 'bill@builtbykrit.com',
        'first_name': 'Bill',
        'last_name': 'Brower',
        'password': 'password125'
    }

    def assert_create_user_response_is_correct(self, response):
        json_data = json.loads(response.content.decode('utf-8'))
        assert 'data' in json_data
        data = json_data['data']
        assert 'attributes' in data
        assert 'id' in data
        assert 'type' in data
        assert data['type'] == 'users'

        attributes = data['attributes']
        assert 'date_joined' in attributes
        assert 'email' in attributes
        assert 'first_name' in attributes
        assert 'last_name' in attributes
        assert 'password' not in attributes
        assert attributes['email'] == self.ACCOUNT_INFO['email']
        assert attributes['first_name'] == self.ACCOUNT_INFO['first_name']
        assert attributes['last_name'] == self.ACCOUNT_INFO['last_name']

    def register(self, account_info, query_params=None):
        client = Client()
        data = {
            'data': {
                'attributes': account_info,
                'type': 'users'
            }
        }
        header = {'Accept': 'application/vnd.api+json'}
        url = '/{}registration/'.format(
            settings.ROOT_URLPREFIX if settings.ROOT_URLPREFIX else '')

        if query_params:
            url += '?{}'.format(urlencode(query_params))

        return client.post(url,
                           content_type='application/vnd.api+json',
                           data=json.dumps(data),
                           **header)

    def test_registration(self):
        response = self.register(self.ACCOUNT_INFO)
        assert response.status_code == 201
        self.assert_create_user_response_is_correct(response)

    def test_registration_with_common_password(self):
        account_info = self.ACCOUNT_INFO.copy()
        account_info['password'] = 'password'
        response = self.register(account_info)
        assert response.status_code == 400

        json_data = json.loads(response.content.decode('utf-8'))
        assert 'errors' in json_data
        assert 'detail' in json_data['errors'][0]
        assert json_data['errors'][0]['detail'] == \
               'This password is too common.'

    def test_registration_with_email_that_is_in_use(self):
        User.objects.create_user(
            email=self.ACCOUNT_INFO['email'],
            first_name=self.ACCOUNT_INFO['first_name'],
            last_name=self.ACCOUNT_INFO['last_name'],
            password=self.ACCOUNT_INFO['password'],
            username=self.ACCOUNT_INFO['email']
        )

        response = self.register(self.ACCOUNT_INFO)
        assert response.status_code == 400

        json_data = json.loads(response.content.decode('utf-8'))
        assert 'errors' in json_data
        assert 'detail' in json_data['errors'][0]
        assert json_data['errors'][0]['detail'] == \
               'Another user is already registered using that email.'

    def test_registration_with_invalid_signup_code(self):
        data = self.ACCOUNT_INFO.copy()
        data['code'] = 'invalid'
        response = self.register(data)
        assert response.status_code == 400

        json_data = json.loads(response.content.decode('utf-8'))
        assert 'errors' in json_data
        assert 'detail' in json_data['errors'][0]
        assert json_data['errors'][0]['detail'] == \
               'That signup code is invalid.'
