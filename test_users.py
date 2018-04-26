"""Test the users and user endpoint on all methods and covers most edge cases
"""
import unittest
import json
import unittest

from app import app
import config

app.config.from_object('config.TestingConfig')


class UserTests(unittest.TestCase):
    """Tests functionality of the API"""


    def setUp(self):
        """Initialize important variables and makes them easily availabe through the self keyword"""
        self.app = app.test_client()
        self.data = json.dumps({"username" : "balotelli", "email" : "balotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        self.existing_user = self.app.post('/api/v1/auth/signup', data=self.data, content_type='application/json')

    # testing api/vi/users
    def test_get_all_users(self):
        """Tests successfully getting all users through the users endpoint"""
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
    
    def test_successful_user_creation(self):
        """Tests successfully creating a new user through the users endpoint"""
        data = json.dumps({"username" : "marcus23", "email" : "marcusrahford44@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("username"), "marcus23")
        self.assertEqual(result.get("email"), "marcusrahford44@gmail.com")
        self.assertEqual(result.get("password"), "secret12345")
        self.assertEqual(response.status_code, 201)
    
    def test_create_user_using_existing_email(self):
        """Tests unsuccessfully creating a new user because of existing email"""
        data = json.dumps({"username" : "john", "email" : "johnmuiya24@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        response2 = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "user with that email already exists")

    def test_create_user_using_unmatching_passwords(self):
        """Tests unsuccessfully creating a new user because of unmatching passwords"""
        data = json.dumps({"username" : "felix", "email" : "felixmutua@gmail.com",
                           "password" : "secret12345", "confirm_password" : "password12345"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_create_user_using_short_passwords(self):
        """Tests unsuccessfully creating a new user because of too short passwords"""
        data = json.dumps({"username" : "moses", "email" : "musamutua@gmail.com",
                           "password" : "123", "confirm_password" : "123"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password should be at least 8 characters")

    def test_create_user_empty_username(self):
        """Tests unsuccessfully creating a new user because of empty username"""
        data = json.dumps({"username" : "", "email" : "lennykmutua@gmail.com", "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"username": "kindly provide a valid username"})
    
    def test_create_user_empty_email(self):
        """Tests unsuccessfully creating a new user because of empty email"""
        data = json.dumps({"username" : "lenny", "email" : "", "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})
    
    def test_create_user_invalid_email(self):
        """Tests unsuccessfully creating a new user because of invalid email"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmugmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})

    def test_create_user_empty_password(self):
        """Tests unsuccessfully creating a new user because of empty password"""
        data = json.dumps({"username" : "lenny", "email" : "lennymutush@gmail.com",
                           "password" : "", # eight whitespaces
                           "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_create_user_empty_confirm_password(self):
        """Tests unsuccessfully creating a new user because of empty confirm_password"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "secret", "confirm_password" : ""})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")
    
    def test_create_user_whitespace_passwords(self):
        """Tests unsuccessfully creating a new user because of providing whitespace passwords"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "        ", "confirm_password" : "        "})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password should be at least 8 characters")


    # testing api/vi/auth/signup
    def test_successful_signup(self):
        """Tests successfully creating a new user through the users endpoint"""
        data = json.dumps({"username" : "marcus", "email" : "marcusrahford@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("username"), "marcus")
        self.assertEqual(result.get("email"), "marcusrahford@gmail.com")
        self.assertEqual(result.get("password"), "secret12345")
        self.assertEqual(response.status_code, 201)
    
    def test_signup_using_existing_email(self):
        """Tests unsuccessfully creating a new user because of existing email"""
        data = json.dumps({"username" : "john", "email" : "johnmuiya@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        response2 = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "user with that email already exists")

    def test_signup_using_unmatching_passwords(self):
        """Tests unsuccessfully creating a new user because of unmatching passwords"""
        data = json.dumps({"username" : "felix", "email" : "felixmutua@gmail.com",
                           "password" : "secret12345", "confirm_password" : "password12345"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password and confirm password should be identical")

    def test_signup_using_short_passwords(self):
        """Tests unsuccessfully creating a new user because of too short passwords"""
        data = json.dumps({"username" : "moses", "email" : "musamutua@gmail.com",
                           "password" : "123", "confirm_password" : "123"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), "password should be at least 8 characters")

    def test_signup_empty_username(self):
        """Tests unsuccessfully creating a new user because of empty username"""
        data = json.dumps({"username" : "", "email" : "lennykmutua@gmail.com", "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"username": "kindly provide a valid username"})
    
    def test_signup_empty_email(self):
        """Tests unsuccessfully creating a new user because of empty email"""
        data = json.dumps({"username" : "lenny", "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})
    
    def test_signup_invalid_email(self):
        """Tests unsuccessfully creating a new user because of invalid email"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmugmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"email": "kindly provide a valid email address"})

    def test_signup_empty_password(self):
        """Tests unsuccessfully creating a new user because of empty password"""
        data = json.dumps({"username" : "lenny", "email" : "lennymutush@gmail.com",
                           "confirm_password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"password": "kindly provide a valid password"})

    def test_signup_empty_confirm_password(self):
        """Tests unsuccessfully creating a new user because of empty confirm_password"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "secret"})
        response = self.app.post('/api/v1/auth/signup', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"confirm_password": "kindly provide a valid confirmation password"})
    
    def test_successfully_getting_one_user(self):
        """Test getting one user using the user's id"""
        response = self.app.get('/api/v1/users/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_user(self):
        """Test getting a user while provideing non-existing id"""
        response = self.app.get('/api/v1/users/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_user(self):
        """Test a successful user update"""
        data = json.dumps({"username" : "balotelli", "email" : "mariobalotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.put('/api/v1/users/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_user(self):
        """Test updating non_existing user"""
        data = json.dumps({"username" : "balotelli", "email" : "mariobalotelli@gmail.com",
                           "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.put('/api/v1/users/99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successfully_deleting_one_user(self):
        """Test a successful user delete"""
        response = self.app.delete('/api/v1/users/2')
        self.assertEqual(response.status_code, 200)
    
    def test_deleting_non_existing_user(self):
        """Test a deleting user that does not exist"""
        response = self.app.delete('/api/v1/users/15')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
