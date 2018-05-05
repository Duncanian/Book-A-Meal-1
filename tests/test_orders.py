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
        """Tests admin successfully getting all order items"""
        response = self.app.get('/api/v2/orders', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
    
    def test_owner_get_all(self):
        """Tests user successfully getting all order items belonging to them"""
        response = self.app.get('/api/v2/orders', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_successful_creation(self):
        """Tests successfully creating a new order item"""
        order = json.dumps({"order_item" : "nyama choma"})
        response = self.app.post(
            '/api/v2/orders', data=order,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_create_empty_name(self):
        """Test unsuccessful order item creation because of empty name"""
        data = json.dumps({"order_item" : ""})
        response = self.app.post(
            '/api/v2/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
