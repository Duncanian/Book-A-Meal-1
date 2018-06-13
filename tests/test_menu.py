"""Test the menu endpoints on all methods and covers most edge cases
"""
import unittest

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class MenuTests(BaseTests):
    """Tests functionality of the menu endpoint"""


    def test_get_one(self):
        """Test user or admin successfully getting a menu option"""
        response = self.app.get('/api/v3/menu/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_get_not_in_menu(self):
        """Test user or admin getting a meal that is not in the menu"""
        response = self.app.get('/api/v3/menu/1', headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_get_non_existing(self):
        """Test getting a menu option while providing non-existing id"""
        response = self.app.get('/api/v3/menu/57', headers=self.user_header)
        self.assertEqual(response.status_code, 404)

    def test_successful_deletion(self):
        """Test a successful menu item deletion"""
        response = self.app.delete('/api/v3/menu/2', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_delete_not_in_menu(self):
        """Test admin deleting a meal that is not in the menu"""
        response = self.app.delete('/api/v3/menu/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_deleting_non_existing(self):
        """Test a deleting menu option that does not exist"""
        response = self.app.delete('/api/v3/menu/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
