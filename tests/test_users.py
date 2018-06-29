"""Test the users endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class UsersTests(BaseTests):
    """Tests functionality of the users endpoint"""


    def test_admin_get_all(self):
        """Tests successfully getting all users"""
        response = self.app.get('/api/v3/users', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_all(self):
        """Tests normal user unauthorized to get get all users"""
        response = self.app.get('/api/v3/users', headers=self.user_header)
        self.assertEqual(response.status_code, 401)

    def test_no_token_get_all(self):
        """Tests unauthorized to get all users without a token"""
        response = self.app.get('/api/v3/users')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token_admin(self):
        """Test invalid token in an admin_required endpoint"""
        invalid_token = {
            "Content-Type" : "application/json",
            "x-access-token" : "eyJ0eXAiOiJK6MTUyNjczNzQ5Nvm2LkbWLZF2RuD32FBvgG8KyM"}
        response = self.app.get(
            '/api/v3/users',
            headers=invalid_token)
        self.assertEqual(response.status_code, 401)

    def test_good_user_creation(self):
        """Tests successfully creating a new user"""
        data = json.dumps({
            "username" : "mark", "email" : "mark@gmail.com",
            "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 201)


    def test_empty_body(self):
        """Test unsuccessful user creation because of empty body"""
        data = json.dumps({})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_existing_email(self):
        """Test unsuccessful user creation because of existing email"""
        data = json.dumps({
            "username" : "john", "email" : "johndoe@gmail.com",
            "password" : "secret12345", "confirm_password" : "secret12345"})
        res = self.app.post( # pylint: disable=W0612
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_diff_passwords(self):
        """Test unsuccessful user creation because of unmatching passwords"""
        data = json.dumps({
            "username" : "felix", "email" : "felix@gmail.com",
            "password" : "12345678", "confirm_password" : "passwordsecret"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_short_passwords(self):
        """Test unsuccessful user creation because of short passwords"""
        data = json.dumps({
            "username" : "moses", "email" : "moses@gmail.com",
            "password" : "1234567", "confirm_password" : "1234567"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_username(self):
        """Test unsuccessful user creation because of empty username"""
        data = json.dumps({
            "username" : "", "email" : "emptyusername@gmail.com",
            "password" : "12345678", "confirm_password" : "12345678"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_email(self):
        """Test unsuccessful user creation because of empty email"""
        data = json.dumps({
            "username" : "empty",
            "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        """Test unsuccessful user creation because of invalid email"""
        data = json.dumps({
            "username" : "lenny", "email" : "invalidemail.com",
            "password" : "secret12345", "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_password(self):
        """Tests unsuccessful user creation because of empty password"""
        data = json.dumps({
            "username" : "lenny", "email" : "lennymutush@gmail.com",
            "password" : "", "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_conf_password(self):
        """Tests unsuccessful user creation because of empty confirm_password"""
        data = json.dumps({
            "username" : "lenny", "email" : "confpassword@gmail.com",
            "password" : "secret", "confirm_password" : ""})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_whitespace_passwords(self):
        """Tests unsuccessful user creation because of whitespace passwords"""
        data = json.dumps({"username" : "lenny", "email" : "lennykmutua@gmail.com",
                           "password" : "        ", "confirm_password" : "        "})
        response = self.app.post(
            '/api/v3/users', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
