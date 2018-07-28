"""Creating the base class for all the other tests"""
import unittest
import json
from unittest import TestCase
from app.app import app


class BaseTestClass(TestCase):
    """Configuring the base test class for all the test cases"""


    @classmethod
    def setUp(self):
        """App configuration setup"""
        
        self.app = app
        self.client = app.test_client()

        self.user_details = {
            'username' : 'ramon',
            'email' : 'ramonomondi@gmail.com',
            'password' : '1234'
        }


        self.user_no_username = {
            'email' : 'torivega@wawa.com',
            'password' : 'qwerty'
        }

        self.user_no_email = {
            'username' : 'ramon',
            'password' : '1234'
        }

        self.user_no_password = {
            'username' : 'ramon',
            'email' : 'ramonomondi@gmail.com'
        }

        self.user_invalid_password = {
            'username' : 'ramon',
            'email' : 'ramonomondi@gmail.com',
            'password' : '1209'
        }

        self.user_invalid_username = {
            'username' : 'ramoon',
            'email' : 'ramonomondi@gmail.com',
            'password' : '1234'
        }

        self.entry_contents = {
            'title' : 'Trip to oblivion',
            'description' : 'Best days of my life'
        }


        self.entry_no_title = {
            'description' : 'This is it'
        }


        self.entry_no_description = {
            'title' : 'You are in for a treat'
        }


    def signup(self):
        response =self.client.post('/auth/signup',
                        data=json.dumps(self.user_details),
                        headers={'content-type':'application/json'})
        return response

    def login(self):
        response = self.client.post('/auth/login',
                        data=json.dumps(self.user_details),
                        headers={'content-type':'application/json'})
        return response                


    @classmethod
    def classTearDown(cls):
        pass


if __name__ == '__main__':
    unittest.main()
