"""Test the menus endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class MenusTests(BaseTests):
    """Tests functionality of the menus endpoint"""


    def test_admin_get_all(self):
        """Test admin successfully getting all menu options"""
        response = self.app.get('/api/v3/menu', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_all(self):
        """Test user successfully getting all menu options"""
        response = self.app.get('/api/v3/menu', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_no_token_get_all(self):
        """Test unauthenticated user unsuccessfully getting all menu options"""
        response = self.app.get('/api/v3/menu')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test invalid token in a token_required endpoint"""
        invalid_token = {
            "Content-Type" : "application/json",
            "x-access-token" : "eyJ0eXAcCI6MTX266RLLk-bWL-ZF2RuD32FBvg_G8KyM"}
        response = self.app.get(
            '/api/v3/menu',
            headers=invalid_token)
        self.assertEqual(response.status_code, 401)

    def test_good_addition(self):
        """Test admin successfully creating a new menu option"""
        data = json.dumps({"meal_id" : 1})
        response = self.app.post(
            '/api/v3/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_adding_existing(self):
        """Test adding meal already in the menu to the menu"""
        data = json.dumps({"meal_id" : 1})
        res = self.app.post( # pylint: disable=W0612
            '/api/v3/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v3/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_addition_empty_id(self):
        """Test unsuccessful menu option creation because of empty meal_id"""
        data = json.dumps({})
        response = self.app.post(
            '/api/v3/menu',data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
