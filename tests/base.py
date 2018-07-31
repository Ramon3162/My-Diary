"""Creating the base class for all the other tests"""
import unittest
import json
from unittest import TestCase
from app.app import app
from app.models import Database
from instance.config import app_config


class BaseTestClass(TestCase):
    """Configuring the base test class for all the test cases"""

    @classmethod
    def setUp(self):
        """App configuration setup"""
        
        self.app = app.config.from_object(app_config['testing'])
        self.client = app.test_client()        

        self.user_details = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com',
            'password' : '123456789'
        }

        self.user_no_username = {
            'email' : 'torivega@wawa.com',
            'password' : 'qwerty'
        }

        self.user_no_email = {
            'username' : 'ramonomondi',
            'password' : '123456789'
        }

        self.user_no_password = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com'
        }

        self.user_invalid_password = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com',
            'password' : '12098899'
        }

        self.user_wrong_username = {
            'username' : 'ramoon',
            'email' : 'ramonomondi@gmail.com',
            'password' : '123456789'
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

    def signup_user(self):
        response =self.client.post('/auth/signup',
                        data=json.dumps(self.user_details),
                        headers={'content-type':'application/json'})
        return response

    def login_user(self):
        response = self.client.post('/auth/login',
                        data=json.dumps(self.user_details),
                        headers={'content-type':'application/json'})
        return response             
 
    def tearDown(self):
        Database().drop_user_table()
        Database().drop_entry_table()

if __name__ == '__main__':
    unittest.main()
