"""Testing for the methods applied to the entries"""
from tests.base import BaseTestClass
from app import app

import unittest
import json


class TestEntryCase(BaseTestClass):
    """Class testing for entry test cases"""


    def test_post_entry(self):
        """Test for posting an entry"""

        # Correct entry format
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_contents),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry created successfully')

        # No title
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_no_title),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Title is required')

        # No description
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_no_description),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Description is required')

        

    def test_get_all_entries(self):
        """Test for viewing all user entries"""

        
        response = self.client.get('/api/v1/entries',
                                    data=json.dumps(self.entry_contents),
                                    content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'All entries found successfully')


    def test_get_single_entry(self):
        """Test for viewing a single entry"""


        response = self.client.get('/api/v1/entries/1',
                                    data=json.dumps(self.entry_contents),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry retrieved successfully')


    def test_update_entry(self):
        """Test for updating an entry"""


        response = self.client.put('/api/v1/entries/1',
                                    data=json.dumps(dict(title="Name")),
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry updated successfully')

    
    def test_delete_entry(self):
        """Test for deleting an entry"""


        response = self.client.delete('/api/v1/entries/0',
                                    content_type=('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry deleted successfully')


if __name__ == '__main__':
    unittest.main()
