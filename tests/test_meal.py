"""Test the meal endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class MealTests(BaseTests):
    """Tests functionality of the meal endpoint"""


    def test_admin_get_one(self):
        """Tests admin successfully getting a meal item"""
        data = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        added_meal = self.app.post( # pylint: disable=W0612
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v2/meals/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user unsuccessfully getting a meal item"""
        data = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        added_meal = self.app.post( # pylint: disable=W0612
            '/api/v2/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v2/meals/1', headers=self.user_header)
        self.assertEqual(response.status_code, 401)

    def test_get_non_existing(self):
        """Test getting a meal item while providing non-existing id"""
        response = self.app.get('/api/v2/meals/10', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_meal_update(self):
        """Test a successful meal item update"""
        initial_data = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        added_meal = self.app.post( # pylint: disable=W0612
            '/api/v2/meals', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        data = json.dumps({"meal_item" : "Pilau with spices", "price" : 600})
        response = self.app.put(
            '/api/v2/meals/1', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_update_non_existing(self):
        """Test updating non_existing meal item"""
        data = json.dumps({"meal_item" : "Pilau with spices", "price" : 600})
        response = self.app.put(
            '/api/v2/meals/12', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful meal item deletion"""
        initial_data = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        added_meal = self.app.post( # pylint: disable=W0612
            '/api/v2/meals', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.delete('/api/v2/meals/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test deleting meal that does not exist"""
        response = self.app.delete('/api/v2/meals/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
