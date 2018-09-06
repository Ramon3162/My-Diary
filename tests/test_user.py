"""Testing for the methods applied to the users"""
import json
from tests.base import BaseTestClass

class TestUserCase(BaseTestClass):
    """Class testing for user cases"""

    def test_signup(self):
        """Testing signup with the correct credentials"""
        response = self.signup_user()
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'User created successfully')

    def test_signup_invalid_username(self):
        """Testing signup with an invalid username"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps({
                                        'username':'Jam##3',
                                        'email': 'json@gmail.com',
                                        'password':'128888834',
                                        'confirm_password':'128888834'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username should not have any special characters.')

    def test_signup_invalid_email(self):
        """Testing signup with an invalid email"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps({
                                        'username':'JamesMwangi',
                                        'email': 'jsongmail.com',
                                        'password':'88881234',
                                        'confirm_password':'88881234'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Invalid email format.')

    def test_signup_short_username(self):
        """Testing signup with a short username"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps({
                                        'username':'Ja',
                                        'email': 'json@gmail.com',
                                        'password':'88881234',
                                        'confirm_password':'88881234'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username should be at least three characters long.')

    def test_signup_short_password(self):
        """Testing signup with a short password"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps({
                                        'username':'JamesMwangi',
                                        'email': 'json@gmail.com',
                                        'password':'1234',
                                        'confirm_password':'1234'}),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password should be at least eight characters long.')

    def test_signup_same_username(self):
        """Testing signup with the same username"""
        self.signup_user()
        response = self.signup_user()
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username already exists')

    def test_signup_no_username(self):
        """Testing signup with no username"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_username),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username is required')

    def test_signup_no_email(self):
        """Testing signup with no email"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_email),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], 'Email is required')

    def test_signup_no_password(self):
        """Testing signup with no password"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is required')

    def test_signup_no_confirm_password(self):
        """Testing signup without confirm password field"""
        response = self.client.post('/auth/signup',
                                    data=json.dumps(self.user_no_confirm_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Confirm password field is required')

    def test_login(self):
        """Testing login with the right credentials"""
        self.signup_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Login successfull')

    def test_login_invalid_password(self):
        """Testing login with an invalid password"""
        self.signup_user()
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_invalid_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is invalid')

    def test_login_invalid_username(self):
        """Testing login with an invalid username"""
        self.signup_user()
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_wrong_username),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username is invalid')

    def test_login_no_username(self):
        """Testing login with no username"""
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_no_username),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Username is required')

    def test_login_no_password(self):
        """Testing login without a password"""
        response = self.client.post('/auth/login',
                                    data=json.dumps(self.user_no_password),
                                    headers={'content-type':'application/json'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'Password is required')

    def test_update_user_data(self):
        """Testing updating a user"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.put('/users/1',
                                   data=json.dumps(self.user_update),
                                   content_type='application/json',
                                   headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'User data updated successfully')

    def test_get_user_data(self):
        """Test for getting user data"""
        self.signup_user()
        login = self.login_user()
        token = json.loads(login.data.decode("UTF-8"))['token']
        response = self.client.get('/users/1',
                                   data=json.dumps(self.user_details),
                                   content_type='application/json',
                                   headers={"Authorization":"Bearer {}".format(token)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'User retrieved successfully')
    