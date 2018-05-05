"""Test the order endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class OrderTests(BaseTests):
    """Tests functionality of the orders endpoint"""

    
    def test_get_one(self):
        """Tests successfully getting an order item"""
        response = self.app.get('/api/v2/orders/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_getting_non_existing(self):
        """Test getting an order_item while providing non-existing id"""
        response = self.app.get('/api/v2/orders/57', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_successful_update(self):
        """Test a successful order item update"""
        meal = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        menu = json.dumps({"menu_option" : "Rice and Beans"})
        order = json.dumps({"order_item" : "Rice and Beans"})
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
            headers=self.admin_header)
        data = json.dumps({"order_item" : "nyama choma"})
        response = self.app.put(
            '/api/v2/orders/2', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_updating_non_existing(self):
        """Test updating non_existing order_item"""
        data = json.dumps({"order_item" : "Pilau with spices"})
        response = self.app.put(
            '/api/v2/orders/45', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_successful_deletion(self):
        """Test a successful order_item deletion"""
        response = self.app.delete('/api/v2/orders/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test a deleting order item that does not exist"""
        response = self.app.delete('/api/v2/orders/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
