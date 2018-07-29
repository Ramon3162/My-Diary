"""Testing for the methods applied to the users"""
from tests.base import BaseTestClass

import json

class TestUserCase(BaseTestClass):
    """Class testing for user cases"""

    def test_signup(self):

        #correct data format
        response = self.client.post('/auth/signup',
                                    data=json.dumps({'username':'James', 'email': 'json@gmail.com','password':'1234'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'User created successfully')

    def test_signup_same_username(self):          
        
        #Same username
        response = self.signup()
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username already exists')

    
    def test_signup_no_username(self):

        #No username
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_username),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username is required')

    def test_signup_no_email(self):

        #No email
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_email),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Email is required')

    def test_signup_no_password(self):

        #No password
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is required')
    
    
    def test_login(self):
        
        #Correct details
        self.signup()
        response = self.login()
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Login successfull')

    
    def test_login_invalid_password(self):
    
        #Invalid password
        self.signup()        
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_invalid_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is invalid')

    
    def test_login_invalid_username(self):

        #Invalid username
        self.signup()        
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_invalid_username),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username is invalid')

    
    def test_login_no_username(self):

        #No username
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_no_username),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username is required')        
        
    
    def test_login_no_password(self):
    
        #No password
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_no_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is required')
    