"""Creating the base class for all the other tests"""
import unittest
import json
from unittest import TestCase
from app import app


class BaseTestClass(TestCase):
    """Configuring the base test class for all the test cases"""

    @classmethod
    def setUp(self):
        """App configuration setup"""
        
        self.app = app
        self.app = self.app.test_client()

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

