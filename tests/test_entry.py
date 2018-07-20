"""Testing for the methods applied to the entries"""
from .base import BaseTestClass
from app.app import app, entries, entry

import unittest
import json

class TestEntryCase(BaseTestClass):
    """Class testing for entry test cases"""

    def setUp(self):
        self.app = app
        self.app = self.app.test_client()
        self.entries = entries
        self.entry = entry


    def test_post_entry(self):
        """Test for posting an entry"""
       
        response = self.app.post('/api/v1/entries', data=json.dumps(self.entry), content_type = ('application/json'))
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry created successfully')

    def test_get_all_entries(self):
        """Test for viewing all user entries"""
        
        response = self.app.get('/api/v1/entries',data=json.dumps(self.entries), content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'All entries found successfully')

    def test_get_single_entry(self):
        """Test for viewing a single entry"""

        response = self.app.get('/api/v1/entries/1', content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry retrieved successfully')

    def test_update_entry(self):
        """Test for updating an entry"""
        
        response = self.app.put('/api/v1/entries/1', data=json.dumps(dict(title="Name")), content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry updated successfully')
    
    def test_delete_entry(self):
        """Test for deleting an entry"""
            
        response = self.app.delete('/api/v1/entries/0', content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry deleted successfully')

if __name__ == '__main__':
    unittest.main()