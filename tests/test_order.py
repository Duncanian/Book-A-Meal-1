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


    def test_admin_get_one(self):
        """Test admin successfully getting an order"""
        response = self.app.get('/api/v3/orders/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Test user successfully getting an order item"""
        response = self.app.get('/api/v3/orders/1', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_getting_non_existing(self):
        """Test getting an order while providing non-existing id"""
        response = self.app.get('/api/v3/orders/57', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_successful_update(self):
        """Test a successful order item update"""
        menu = json.dumps({"name" : "beans", "price" : "20", "in_menu" : True})
        create_menu = self.app.post( # pylint: disable=W0612
            '/api/v3/meals', data=menu, content_type='application/json',
            headers=self.admin_header)
        data = json.dumps({"meal_id" : 3})
        response = self.app.put(
            '/api/v3/orders/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_updating_non_existing(self):
        """Test updating non_existing order_item"""
        data = json.dumps({"meal_id" : 3})
        response = self.app.put(
            '/api/v3/orders/45', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_update_no_change(self):
        """Test an order update providing the same meal_id as previously"""
        data = json.dumps({"meal_id" : 2})
        response = self.app.put(
            '/api/v3/orders/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_update_meal_not_in_menu(self):
        """Test an order update to meal not in menu"""
        data = json.dumps({"meal_id" : 1})
        response = self.app.put(
            '/api/v3/orders/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_missing_in_menu(self):
        """Test an order update with missing in menu value"""
        data = json.dumps({})
        response = self.app.put(
            '/api/v3/orders/1',data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_successful_deletion(self):
        """Test a successful order_item deletion"""
        response = self.app.delete('/api/v3/orders/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test a deleting order item that does not exist"""
        response = self.app.delete('/api/v3/orders/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_not_owner_get(self):
        """Test user who's not owner trying to get a particular order"""
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
        response = self.app.get('/api/v3/orders/1', headers=user_header)
        self.assertEqual(response.status_code, 404)

    def test_not_owner_update(self):
        """Test user who's not owner trying to update a particular order"""
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
        data = json.dumps({"meal_id" : 3})
        response = self.app.put(
            '/api/v3/orders/1', data=data,
            content_type='application/json',
            headers=user_header)
        self.assertEqual(response.status_code, 401)

    def test_not_owner_delete(self):
        """Test user who's not owner trying to delete a particular order"""
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
        response = self.app.delete('/api/v3/orders/1', headers=user_header)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
