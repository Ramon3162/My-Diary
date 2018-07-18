"""Creating the base class for all the other tests"""
import unittest
import json
from unittest import TestCase
from app import app


class BaseTestClass(TestCase):
    """Configuring the base test class for all the test cases"""

    @classmethod
    def classSetup(self):
        """App configuration setup"""
        
        self.app = app
        self.client = self.app.test_client()
        

        self.entry_contents = {
            'title' : 'Trip to oblivion',
            'description' : 'Best days of my life',
        }

        self.entry_no_title = {
            'description' : 'This is it'
        }

        self.entry_no_description = {
            'title' : 'You are in for a treat'
        }

    @classmethod
    def classTearDown(cls):
        pass

if __name__ == '__main__':
    unittest.main()
