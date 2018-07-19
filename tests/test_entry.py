"""Testing for the methods applied to the entries"""
from tests.base import BaseTestClass

import json

class TestEntryCase(BaseTestClass):
    """Class testing for entry test cases"""

    def test_post_entry(self):
        """Test for posting an entry"""
        
        #Not JSON data
        response = self.app.post('/api/v1/entries/', data=json.dumps(self.entry_contents))
        self.assertEqual(response.status_code, 400)

        #No title
        response = self.app.post('/api/v1/entries', data=json.dumps(self.entry_no_title), content_type = ('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Title should be a string')

        #No description
        response = self.app.post('/api/v1/entries', data=json.dumps(self.entry_no_description), content_type = ('application/json'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Description should be a string')

        #The correct request
        response = self.app.post('/api/v1/entries', data=json.dumps(self.entry_contents), content_type = ('application/json'))
        self.assertEqual(data['message'], 'Entry created successfully')

    def test_get_all_entries(self):
        """Test for viewing all user entries"""
        
        response = self.app.get('/api/v1/entries', data=json.dumps(self.entry_contents), content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entries found successfully')

    def test_get_single_entry(self):
        """Test for viewing a single entry"""
        
        response = self.app.get('/api/v1/entries/1', data=json.dumps(self.entry_contents), content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry retrieved successfully')

    def test_update_entry(self):
        """Test for updating an entry"""
        
        response = self.app.put('/api/v1/entries/1', data=json.dumps(dict(title="New Title")), content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry updated successfully')
    
    def test_delete_entry(self):
        """Test for deleting an entry"""
            
        response = self.app.delete('/api/v1/entries/1', data=json.dumps(self.entry_contents), content_type = ('application/json'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry deleted successfully')

