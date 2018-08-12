"""Testing for the methods applied to the entries"""
import json
from tests.base import BaseTestClass

class TestEntryCase(BaseTestClass):
    """Class testing for entry test cases"""


    def test_post_entry(self):
        """Test for posting an entry"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_contents),
                                    content_type='application/json',
                                    headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry created successfully')


    def test_post_entry_no_title(self):
        """Test posting an entry with no title"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_no_title),
                                    content_type='application/json',
                                    headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Title is required')

    def test_post_entry_no_description(self):
        """Test posting an entry with no description"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_no_description),
                                    content_type='application/json',
                                    headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Description is required')

    def test_post_entry_empty_title(self):
        """Test posting an entry with only spaces in the title"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_empty_title),
                                    content_type='application/json',
                                    headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry title cannot be empty.')

    def test_post_entry_empty_description(self):
        """Test posting an entry with only spaces in the title"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_empty_description),
                                    content_type='application/json',
                                    headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry description cannot be empty.')

    def test_post_duplicate_entry(self):
        """Test posting an already existing entry"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        self.client.post('/api/v1/entries',
                         data=json.dumps(self.entry_contents),
                         content_type='application/json',
                         headers={"Authorization":"Bearer {}".format(token)})
        response = self.client.post('/api/v1/entries',
                                    data=json.dumps(self.entry_contents),
                                    content_type='application/json',
                                    headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'You cannot publish a duplicate entry.')

    def test_get_all_entries(self):
        """Test for viewing all user entries"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        self.client.post('/api/v1/entries',
                         data=json.dumps(self.entry_contents),
                         content_type='application/json',
                         headers={"Authorization":"Bearer {}".format(token)})
        response = self.client.get('/api/v1/entries',
                                   data=json.dumps(self.entry_contents),
                                   content_type='application/json',
                                   headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'All entries found successfully')

    def test_get_single_entry(self):
        """Test for viewing a single entry"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        self.client.post('/api/v1/entries',
                         data=json.dumps(self.entry_contents),
                         content_type='application/json',
                         headers={"Authorization":"Bearer {}".format(token)})
        response = self.client.get('/api/v1/entries/1',
                                   data=json.dumps(self.entry_contents),
                                   content_type='application/json',
                                   headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry retrieved successfully')

    def test_update_entry(self):
        """Test for updating an entry"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        self.client.post('/api/v1/entries',
                         data=json.dumps(self.entry_contents),
                         content_type='application/json',
                         headers={"Authorization":"Bearer {}".format(token)})
        response = self.client.put('/api/v1/entries/1',
                                   data=json.dumps({
                                       'title':'My Name',
                                       'description':'You know who I am son'}),
                                   content_type='application/json',
                                   headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry updated successfully')

    def test_delete_entry(self):
        """Test for deleting an entry"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        self.client.post('/api/v1/entries',
                         data=json.dumps(self.entry_contents),
                         content_type='application/json',
                         headers={"Authorization":"Bearer {}".format(token)})
        response = self.client.delete('/api/v1/entries/1',
                                      content_type='application/json',
                                      headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry deleted successfully')

    def test_delete_entry_non_existent(self):
        """Test for deleting an entry"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        self.client.post('/api/v1/entries',
                         data=json.dumps(self.entry_contents),
                         content_type='application/json',
                         headers={"Authorization":"Bearer {}".format(token)})
        response = self.client.delete('/api/v1/entries/5',
                                      content_type='application/json',
                                      headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Entry not found.')
