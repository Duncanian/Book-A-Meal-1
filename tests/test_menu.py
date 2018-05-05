"""Test the menu endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class MenuTests(BaseTests):
    """Tests functionality of the menu endpoint"""


    def test_get_one(self):
        """Test user or admin successfully getting a menu option"""
        response = self.app.get('/api/v2/menu/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a menu option while providing non-existing id"""
        response = self.app.get('/api/v2/menu/57', headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_successful_update(self):
        """Test a successful menu option update"""
        meal = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        menu = json.dumps({"menu_option" : "Rice and Beans"})
        updated_meal = json.dumps({"meal_item" : "Pilau with spices", "price" : 600})

        response = self.app.post(
            '/api/v2/meals', data=meal,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v2/meals', data=updated_meal,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v2/menu', data=menu,
            content_type='application/json',
            headers=self.admin_header)
        data = json.dumps({"menu_option" : "Pilau with spices"})
        response = self.app.put(
            '/api/v2/menu/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_updating_non_existing(self):
        """Test updating non_existing menu option"""
        data = json.dumps({"menu_option" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v2/menu/25', data=data,
        content_type='application/json', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_successful_deletion(self):
        """Test a successful menu item deletion"""
        response = self.app.delete('/api/v2/menu/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test a deleting menu item that does not exist"""
        response = self.app.delete('/api/v2/menu/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
