"""Testing for the methods applied to the users"""
from tests.base import BaseTestClass

import json

class TestUserCase(BaseTestClass):
    """Class testing for user cases"""

    def test_signup(self):

        #correct data format
        response = self.client.post('/auth/signup',
                                    data=json.dumps({'username':'JamesMwangi', 'email': 'json@gmail.com','password':'12345678'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'User created successfully')
    
    def test_signup_invalid_username(self):
        #invalid username

        response = self.client.post('/auth/signup',
                                    data=json.dumps({'username':'Jam##3', 'email': 'json@gmail.com','password':'128888834'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username should not have any special characters.')

    def test_signup_invalid_email(self):
        #invalid email

        response = self.client.post('/auth/signup',
                                    data=json.dumps({'username':'JamesMwangi', 'email': 'jsongmail.com','password':'88881234'}),
                                    headers={'content-type':'application/json'})
        print(response.data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Invalid email format.')

    def test_signup_short_username(self):
        #short username

        response = self.client.post('/auth/signup',
                                    data=json.dumps({'username':'Ja', 'email': 'json@gmail.com','password':'88881234'}),
                                    headers={'content-type':'application/json'})
        print(response.data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username should be at least three characters long.')

    def test_signup_short_password(self):
        #invalid email

        response = self.client.post('/auth/signup',
                                    data=json.dumps({'username':'JamesMwangi', 'email': 'json@gmail.com','password':'1234'}),
                                    headers={'content-type':'application/json'})
        print(response.data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password should be at least eight characters long.')


    def test_signup_same_username(self):          
        
        #Same username
        self.signup_user()
        response = self.signup_user()
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
        self.signup_user()
        response = self.login_user()
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Login successfull')

    
    def test_login_invalid_password(self):
    
        #Invalid password
        self.signup_user()        
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_invalid_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is invalid')

    
    def test_login_invalid_username(self):

        #Invalid username
        self.signup_user()        
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_wrong_username),
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
    