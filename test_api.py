import json
import unittest

from app import app
import config

app.config.from_object('config.TestingConfig')


class APITestCase(unittest.TestCase):
    """Tests all functionality of the API"""


    def setUp(self):
        """Initialize important variables and makes them easily availabe through the self keyword"""
        self.app = app.test_client()
       
    def test_get_all_users(self):
        """Tests successfully getting all users through the users endpoint"""
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def test_creating_new_user(self):
        """Tests successfully creating a new user through the users endpoint"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "secret", "confirm_password" : "secret"})
        response = self.app.post('/api/v1/users', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result["username"], "lenny")
        self.assertEqual(result["email"], "lennykmutua@gmail.com")
        self.assertEqual(result["password"], "secret")
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
