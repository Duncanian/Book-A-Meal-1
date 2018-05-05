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

    def test_successful_creation(self):
        """Tests successfully creating a new order item"""
        meal = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        menu = json.dumps({"menu_option" : "Rice and Beans", "price" : 400})
        order = json.dumps({"order_item" : "Rice and Beans", "price" : 400})
        response = self.app.post(
            '/api/v2/meals', data=meal,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v2/menu', data=menu,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v2/orders', data=order,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_create_empty_name(self):
        """Test unsuccessful order item creation because of empty name"""
        data = json.dumps({"order_item" : "", "price" : 400})
        response = self.app.post(
            '/api/v2/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_create_empty_price(self):
        """Tests unsuccessful order item creation because of empty price"""
        data = json.dumps({"order_item" : "Ugali and Kuku", "price" : ""})
        response = self.app.post(
            '/api/v2/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_price(self):
        """Tests unsuccessful order item creation because of invalid price"""
        data = json.dumps({"order_item" : "Mchele and Pork", "price" : "one hundred"})
        response = self.app.post(
            '/api/v2/orders', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
