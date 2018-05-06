"""Test the meals endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class MealsTests(BaseTests):
    """Tests functionality of the meals endpoint"""


    def test_admin_get_all(self):
        """Test admin successfully getting all meals"""
        response = self.app.get('/api/v2/meals', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_all(self):
        """Test user unsuccessfully getting all meals"""
        response = self.app.get('/api/v2/meals', headers=self.user_header)
        self.assertEqual(response.status_code, 401)

    def test_no_token_get_all(self):
        """Tests unauthenticated user unsuccessfully getting all meals"""
        response = self.app.get('/api/v2/meals')
        self.assertEqual(response.status_code, 401)

    def test_good_meal_creation(self):
        """Tests successfully creating a new meal item"""
        data = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        response = self.app.post(
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 201)

    def test_meal_existing_name(self):
        """Test unsuccessful meal creation because of existing meal item name"""
        data = json.dumps({"meal_item" : "Fries and Chicken", "price" : 400})
        res = self.app.post( # pylint: disable=W0612
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_meal_empty_name(self):
        """Tests unsuccessful meal creation because of empty meal item"""
        data = json.dumps({"meal_item" : "", "price" : 400})
        response = self.app.post(
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_meal_empty_price(self):
        """Tests unsuccessful meal creation because of empty price"""
        data = json.dumps({"meal_item" : "Ugali and Chicken", "price" : ""})
        response = self.app.post(
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_meal_invalid_price(self):
        """Tests unsuccessful meal creation because of invalid price"""
        data = json.dumps({"meal_item" : "Ugali", "price" : "four hundred"})
        response = self.app.post(
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
