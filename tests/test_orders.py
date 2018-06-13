"""Test the orders endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class OrdersTests(BaseTests):
    """Tests functionality of the orders endpoint"""


    def test_get_all(self):
        """Test admin successfully getting all order items"""
        response = self.app.get('/api/v3/orders', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_owner_get_all(self):
        """Test user successfully getting all order items belonging to him"""
        response = self.app.get('/api/v3/orders', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_successful_creation(self):
        """Tests successfully creating a new order item"""
        data = json.dumps({"meal_id" : 2})
        response = self.app.post(
            '/api/v3/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 201)

    def test_not_in_menu(self):
        """Tests creating an order of meal not in menu"""
        data = json.dumps({"meal_id" : 1})
        response = self.app.post(
            '/api/v3/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_create_empty_id(self):
        """Test unsuccessful order creation because of empty id"""
        data = json.dumps({"meal_id" : ""})
        response = self.app.post(
            '/api/v3/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
