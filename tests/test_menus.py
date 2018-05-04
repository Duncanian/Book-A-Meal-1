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
        response = self.app.get('/api/v2/menu', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_all(self):
        """Test user successfully getting all menu options"""
        response = self.app.get('/api/v2/menu', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_no_token_get_all(self):
        """Test unauthenticated user unsuccessfully getting all menu options"""
        response = self.app.get('/api/v2/menu')
        self.assertEqual(response.status_code, 401)

    def test_good_creation(self):
        """Test admin successfully creating a new menu option"""
        data = json.dumps({"menu_option" : "Rice and Beans", "price" : 400})
        response = self.app.post(
            '/api/v2/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 201)

    def test_creation_existing_name(self):
        """Tests unsuccessful menu option creation because of existing name"""
        data = json.dumps({"menu_option" : "Fries and Chicken", "price" : 400})
        res = self.app.post( # pylint: disable=W0612
            '/api/v2/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v2/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_creation_empty_name(self):
        """Tests unsuccessful menu option creation because of empty name"""
        data = json.dumps({"menu_option" : "", "price" : 400})
        response = self.app.post(
            '/api/v2/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_creation_empty_price(self):
        """Tests unsuccessful menu option creation because of empty price"""
        data = json.dumps({"menu_option" : "Ugali and Kuku", "price" : ""})
        response = self.app.post(
            '/api/v2/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_creation_invalid_price(self):
        """Tests unsuccessful menu option creation because of invalid price"""
        data = json.dumps({"menu_option" : "Mchele and Pork", "price" : "351.9"})
        response = self.app.post(
            '/api/v2/menu', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()