"""Test the user endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class UsersTest(BaseTests):
    """Tests functionality of the user endpoint"""


    def test_admin_get_user(self):
        """Test admin getting one user by providing the user_id"""
        response = self.app.get('/api/v3/users/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_user(self):
        """Test non-admin user getting one user by providing the user_id"""
        response = self.app.get('/api/v3/users/1', headers=self.user_header)
        self.assertEqual(response.status_code, 401)

    def test_get_non_existing(self):
        """Test getting a user while providing non-existing id"""
        response = self.app.get('/api/v3/users/27', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_update(self):
        """Test a successful user update"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecret1", "confirm_password" : "topsecret1"})
        response = self.app.put(
            '/api/v3/users/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_update_short_password(self):
        """Test unsuccessful user update because of short password"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecr", "confirm_password" : "topsecr"})
        response = self.app.put(
            '/api/v3/users/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_update_diff_passwords(self):
        """Test unsuccessful user update because of unmatching passwords"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecret157", "confirm_password" : "topsecret1"})
        response = self.app.put(
            '/api/v3/users/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_updating_non_existing(self):
        """Test updating non_existing user"""
        data = json.dumps({
            "username" : "user1", "email" : "user1@gmail.com",
            "password" : "topsecret1", "confirm_password" : "topsecret1"})
        response = self.app.put(
            '/api/v3/users/55', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful user deletion"""
        response = self.app.delete('/api/v3/users/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existing(self):
        """Test a deleting user that does not exist"""
        response = self.app.delete('/api/v3/users/5', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_not_owner_delete(self):
        """Test user who's not owner trying to delete account"""
        user_reg = json.dumps({
            "username" : "user22",
            "email" : "user22@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678"})
        user_log = json.dumps({
            "email" : "user22@gmail.com",
            "password" : "12345678"})
        register_user = self.app.post( # pylint: disable=W0612
            '/api/v3/auth/signup', data=user_reg,
            content_type='application/json')
        user_result = self.app.post(
            '/api/v3/auth/login', data=user_log,
            content_type='application/json')
        user_response = json.loads(user_result.get_data(as_text=True))
        user_token = user_response["token"]
        user_header = {"Content-Type" : "application/json", "x-access-token" : user_token}
        response = self.app.delete('/api/v3/users/1', headers=user_header)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
