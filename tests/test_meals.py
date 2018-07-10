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
        response = self.app.get('/api/v3/meals', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_all(self):
        """Test user unsuccessfully getting all meals"""
        response = self.app.get('/api/v3/meals', headers=self.user_header)
        self.assertEqual(response.status_code, 401)

    def test_no_token_get_all(self):
        """Tests unauthenticated user unsuccessfully getting all meals"""
        response = self.app.get('/api/v3/meals')
        self.assertEqual(response.status_code, 401)

    def test_good_meal_creation(self):
        """Tests successfully creating a new meal"""
        data = json.dumps({"name" : "Rice and Beans", "price" : 400, "in_menu" : False})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 201)

    def test_existing_name(self):
        """Test unsuccessful meal creation because of existing meal name"""
        data = json.dumps({"name" : "Fries and Chicken", "price" : 400, "in_menu" : False})
        res = self.app.post( # pylint: disable=W0612
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_name(self):
        """Tests unsuccessful meal creation because of empty name"""
        data = json.dumps({"price" : 400, "in_menu" : False})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_invalid_name(self):
        """Tests unsuccessful meal creation because of invalid name"""
        data = json.dumps({"name" : "   ", "price" : 400, "in_menu" : False})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_price(self):
        """Tests unsuccessful meal creation because of empty price"""
        data = json.dumps({"name" : "Ugali and Chicken", "in_menu" : False})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_invalid_price(self):
        """Tests unsuccessful meal creation because of invalid price"""
        data = json.dumps({"name" : "Ugali", "price" : "four hundred", "in_menu" : False})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_in_menu(self):
        """Tests unsuccessful meal creation because of empty in_menu boolean"""
        data = json.dumps({"name" : "Ugali and Chicken", "price" : 400})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)

    def test_invalid_in_menu(self):
        """Tests unsuccessful meal creation because of invalid in_menu boolean"""
        data = json.dumps({"name" : "Ugali", "price" : 400, "in_menu" : "present"})
        response = self.app.post(
            '/api/v3/meals', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
