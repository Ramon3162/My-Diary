"""Creating the base class for all the other tests"""
import json
import unittest

from app.app import app
from app.database import Database


class BaseTestClass(unittest.TestCase):
    """Configuring the base test class for all the test cases"""

    def setUp(self):
        """App configuration setup"""
        self.client = app.test_client()

        self.user_details = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com',
            'password' : '123456789',
            'confirm_password': '123456789'
        }

        self.user_login_details = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com',
            'password' : '123456789'
        }

        self.user_no_username = {
            'email' : 'torivega@wawa.com',
            'password' : 'qwerty',
            'confirm_password' : 'qwerty'
        }

        self.user_no_email = {
            'username' : 'ramonomondi',
            'password' : '123456789',
            'confirm_password' : '123456789'
        }

        self.user_no_password = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com',
            'confirm_password' : '123456789'
        }

        self.user_no_confirm_password = {
            'username' : 'ramonomondi',
            'email' : 'ramonomondi@gmail.com',
            'password' : '123456789'
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

        self.user_update = {
            'username' : 'Ian',
            'email' : 'ramonomondi@gmail.com',
            'status' : 'Life is fleeting'
        }

        self.entry_contents = {
            'title' : 'Trip to oblivion',
            'description' : 'Best days of my life'
        }

        self.entry_no_title = {
            'description' : 'This is it'
        }

        self.entry_empty_title = {
            'title': ' ',
            'description' : 'This is it'
        }

        self.entry_no_description = {
            'title' : 'You are in for a treat'
        }

        self.entry_empty_description = {
            'title' : 'You are in for a treat',
            'description' : ' '
        }

    def signup_user(self):
        """Method to register a user"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_details),
                                    headers={'content-type':'application/json'})
        return response

    def login_user(self):
        """Method to log in a user"""
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_login_details),
                                    headers={'content-type':'application/json'})
        return response

    def tearDown(self):
        Database().drop_user_table()
        Database().drop_entry_table()

if __name__ == '__main__':
    unittest.main()
