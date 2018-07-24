"""Testing for the methods applied to the users"""
from tests.base import BaseTestClass
from app import app

import unittest
import json

class TestUserCase(BaseTestClass):
    """Class testing for user cases"""

    def test_login(self):
        
        #Correct details
        response = self.client.post('/api/vi/user/login',
                                    data=json.dumps(self.user),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Login successfully')

        #No username
        response = self.client.post('/api/v1/user/login',
                                    data=json.dumps(self.user_no_username),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data('message'), 'Username is required')

        #No password
        response = self.client.post('/api/v1/user/login',
                                    data=json.dumps(self.user_no_password),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is required')

    def test_signin(self):

        
        #Correct details
        response = self.client.post('/api/v1/user/signin',
                                    data=json.dumps(self.user),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'User created successfully')

        #No username
        response = self.client.post('/api/v1/user/signin',
                                    data=json.dumps(self.user_no_username),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data('message'), 'Username is required')

        #No email
        response = self.client.post('/api/v1/user/signin',
                                    data=json.dumps(self.user_no_email),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data)
        self.assertEqual(data['message'], 'Email is required')

        #No password
        response = self.client.post('/api/v1/user/signin',
                                    data=json.dumps(self.user_no_password),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is required')
