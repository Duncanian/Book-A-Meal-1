"""Test the meals and menu endpoints on all methods and covers most edge cases
"""
import unittest
import json
import unittest

from app import app
import config

app.config.from_object('config.TestingConfig')


class MealTests(unittest.TestCase):
    """Tests functionality of the API"""


    def setUp(self):
        """Initialize important variables and makes them easily availabe through the self keyword"""
        self.app = app.test_client()
        self.data = json.dumps({"name" : "Spicy Pilau", "price" : 600})
        self.existing_meal = self.app.post('/api/v1/meals', data=self.data, content_type='application/json')
        self.existing_menu = self.app.post('/api/v1/menu', data=self.data, content_type='application/json')
    
    def test_get_all_meals(self):
        """Tests successfully getting all meals through the meals endpoint"""
        response = self.app.get('/api/v1/meals')
        self.assertEqual(response.status_code, 200)

    def test_successful_meal_creation(self):
        """Tests successfully creating a new meal through the meals endpoint"""
        data = json.dumps({"name" : "Rice and Beans", "price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("name"), "Rice and Beans")
        self.assertEqual(result.get("price"), '400')
        self.assertEqual(response.status_code, 201)

    def test_create_meal_using_existing_name(self):
        """Tests unsuccessfully creating a new meal because of existing name"""
        data = json.dumps({"name" : "Fries and Chicken", "price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        response2 = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "Meal with that name already exists")
    
    def test_create_meal_empty_name(self):
        """Tests unsuccessfully creating a new meal because of empty name"""
        data = json.dumps({"price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"name": "no name provided"})
    
    def test_create_meal_empty_price(self):
        """Tests unsuccessfully creating a new meal because of empty price"""
        data = json.dumps({"name" : "Ugali and Chicken"})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "no price provided"})

    def test_get_one_meal(self):
        """Tests successfully getting a meal through the meals endpoint"""
        response = self.app.get('/api/v1/meals/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_meal(self):
        """Test getting a meal while providing non-existing id"""
        response = self.app.get('/api/v1/meals/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_meal(self):
        """Test a successful meal update"""
        data = json.dumps({"name" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/meals/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_meal(self):
        """Test updating non_existing meal"""
        data = json.dumps({"name" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/meals/99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_deleting_one_meal(self):
        """Test a successful meal deletion"""
        response = self.app.delete('/api/v1/meals/2')
        self.assertEqual(response.status_code, 200)
    
    def test_deleting_non_existing_meal(self):
        """Test a deleting meal that does not exist"""
        response = self.app.delete('/api/v1/meals/15')
        self.assertEqual(response.status_code, 404)



    # Menu Item tests
    def test_get_all_menu(self):
        """Tests successfully getting all menu items through the meals endpoint"""
        response = self.app.get('/api/v1/menu')
        self.assertEqual(response.status_code, 200)

    def test_successful_menu_creation(self):
        """Tests successfully creating a new menu item through the menu endpoint"""
        data = json.dumps({"name" : "Rice and Beans", "price" : 400})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("name"), "Rice and Beans")
        self.assertEqual(result.get("price"), '400')
        self.assertEqual(response.status_code, 201)

    def test_create_menu_using_existing_name(self):
        """Tests unsuccessfully creating a new menu item because of existing name"""
        data = json.dumps({"name" : "Fries and Chicken", "price" : 400})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        response2 = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "Meal with that name already exists")
    
    def test_create_menu_empty_name(self):
        """Tests unsuccessfully creating a new meal because of empty name"""
        data = json.dumps({"price" : 400})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"name": "no name provided"})
    
    def test_create_menu_empty_price(self):
        """Tests unsuccessfully creating a new menu item because of empty price"""
        data = json.dumps({"name" : "Ugali and Chicken"})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "no price provided"})

    def test_get_one_menu(self):
        """Tests successfully getting a menu item through the menu endpoint"""
        response = self.app.get('/api/v1/menu/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_menu(self):
        """Test getting a menu item while providing non-existing id"""
        response = self.app.get('/api/v1/menu/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_menu(self):
        """Test a successful menu item update"""
        data = json.dumps({"name" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/menu/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_menu(self):
        """Test updating non_existing menu item"""
        data = json.dumps({"name" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/menu/99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_deleting_one_menu(self):
        """Test a successful menu item deletion"""
        response = self.app.delete('/api/v1/menu/2')
        self.assertEqual(response.status_code, 200)
    
    def test_deleting_non_existing_menu(self):
        """Test a deleting menu item that does not exist"""
        response = self.app.delete('/api/v1/menu/15')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
