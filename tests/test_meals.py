"""Test the meals and menu endpoints on all methods and covers most edge cases
"""
import unittest
import json
import unittest

import sys, os # fix import errors
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import app

app = app.create_app()
app.config.from_object('config.TestingConfig')


class MealTests(unittest.TestCase):
    """Tests functionality of the API"""


    def setUp(self):
        """Initialize important variables and makes them easily availabe through the self keyword"""
        self.app = app.test_client()
        self.meal = json.dumps({"meal_item" : "Spicy Pilau", "price" : 600})
        self.menu = json.dumps({"menu_option" : "Spicy Pilau", "price" : 600})
        self.order = json.dumps({"order_item" : "Spicy Pilau", "price" : 600})
        self.existing_meal = self.app.post('/api/v1/meals', data=self.meal, content_type='application/json')
        self.existing_menu = self.app.post('/api/v1/menu', data=self.menu, content_type='application/json')
        self.existing_order = self.app.post('/api/v1/orders', data=self.order, content_type='application/json')
    
    def test_get_all_meals(self):
        """Tests successfully getting all meals through the meals endpoint"""
        response = self.app.get('/api/v1/meals')
        self.assertEqual(response.status_code, 200)

    def test_successful_meal_creation(self):
        """Tests successfully creating a new meal through the meals endpoint"""
        data = json.dumps({"meal_item" : "Rice and Beans", "price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("meal_item"), "Rice and Beans")
        self.assertEqual(result.get("price"), 400.0)
        self.assertEqual(response.status_code, 201)

    def test_create_meal_using_existing_name(self):
        """Tests unsuccessfully creating a new meal because of existing meal item name"""
        data = json.dumps({"meal_item" : "Fries and Chicken", "price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json') # pylint: disable=W0612
        response2 = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "meal item with that name already exists")
    
    def test_create_meal_empty_name(self):
        """Tests unsuccessfully creating a new meal because of empty meal item"""
        data = json.dumps({"meal_item" : "", "price" : 400})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"meal_item": "kindly provide a meal item"})
    
    def test_create_meal_empty_price(self):
        """Tests unsuccessfully creating a new meal because of empty price"""
        data = json.dumps({"meal_item" : "Ugali and Chicken", "price" : ""})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "kindly provide a price(should be a valid number)"})
    
    def test_create_meal_invalid_price(self):
        """Tests unsuccessfully creating a new meal because of empty price"""
        data = json.dumps({"meal_item" : "Ugali", "price" : "four hundred"})
        response = self.app.post('/api/v1/meals', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "kindly provide a price(should be a valid number)"})

    def test_get_one_meal(self):
        """Tests successfully getting a meal item through the meals endpoint"""
        response = self.app.get('/api/v1/meals/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_meal(self):
        """Test getting a meal item while providing non-existing id"""
        response = self.app.get('/api/v1/meals/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_meal(self):
        """Test a successful meal item update"""
        data = json.dumps({"meal_item" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/meals/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_meal(self):
        """Test updating non_existing meal item"""
        data = json.dumps({"meal_item" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/meals/99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_deleting_one_meal(self):
        """Test a successful meal item deletion"""
        response = self.app.delete('/api/v1/meals/2')
        self.assertEqual(response.status_code, 200)
    
    def test_deleting_non_existing_meal(self):
        """Test a deleting meal that does not exist"""
        response = self.app.delete('/api/v1/meals/15')
        self.assertEqual(response.status_code, 404)



    # Menu Item tests
    def test_get_all_menu(self):
        """Tests successfully getting all menu options through the menu endpoint"""
        response = self.app.get('/api/v1/menu')
        self.assertEqual(response.status_code, 200)

    def test_successful_menu_creation(self):
        """Tests successfully creating a new menu options through the menu endpoint"""
        data = json.dumps({"menu_option" : "Rice and Beans", "price" : 400})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("menu_option"), "Rice and Beans")
        self.assertEqual(result.get("price"), 400.0)
        self.assertEqual(response.status_code, 201)

    def test_create_menu_using_existing_name(self):
        """Tests unsuccessfully creating a new menu option because of existing name"""
        data = json.dumps({"menu_option" : "Fries and Chicken", "price" : 400})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json') # pylint: disable=W0612
        response2 = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), "menu option with that name already exists")
    
    def test_create_menu_empty_name(self):
        """Tests unsuccessfully creating a new menu_option because of empty name"""
        data = json.dumps({"menu_option" : "", "price" : 400})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"menu_option": "kindly provide a menu option"})
    
    def test_create_menu_empty_price(self):
        """Tests unsuccessfully creating a new menu item because of empty price"""
        data = json.dumps({"menu_option" : "Ugali and Kuku", "price" : ""})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "kindly provide a price(should be a valid number)"})
    
    def test_create_menu_invalid_price(self):
        """Tests unsuccessfully creating a new menu item because of invalid price"""
        data = json.dumps({"menu_option" : "Mchele and Pork", "price" : "one hundred"})
        response = self.app.post('/api/v1/menu', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "kindly provide a price(should be a valid number)"})

    def test_get_one_menu(self):
        """Tests successfully getting a menu option through the menu endpoint"""
        response = self.app.get('/api/v1/menu/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_menu(self):
        """Test getting a menu option while providing non-existing id"""
        response = self.app.get('/api/v1/menu/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_menu(self):
        """Test a successful menu option update"""
        data = json.dumps({"menu_option" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/menu/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_menu(self):
        """Test updating non_existing menu option"""
        data = json.dumps({"menu_option" : "Pilau with spices", "price" : 600})
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
    

    # Order Item tests
    def test_get_all_orders(self):
        """Tests successfully getting all order items through the orders endpoint"""
        response = self.app.get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)

    def test_successful_order_creation(self):
        """Tests successfully creating a new order item through the orders endpoint"""
        data = json.dumps({"order_item" : "Rice and Beans", "price" : 400})
        response = self.app.post('/api/v1/orders', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("order_item"), "Rice and Beans")
        self.assertEqual(result.get("price"), 400.0)
        self.assertEqual(response.status_code, 201)

    def test_create_order_empty_name(self):
        """Tests unsuccessfully creating a new order_item because of empty name"""
        data = json.dumps({"order_item" : "", "price" : 400})
        response = self.app.post('/api/v1/orders', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"order_item": "kindly provide an order item"})
    
    def test_create_order_empty_price(self):
        """Tests unsuccessfully creating a new order item because of empty price"""
        data = json.dumps({"order_item" : "Ugali and Kuku", "price" : ""})
        response = self.app.post('/api/v1/orders', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "kindly provide a price(should be a valid number)"})
    
    def test_create_order_invalid_price(self):
        """Tests unsuccessfully creating a new order item because of invalid price"""
        data = json.dumps({"order_item" : "Mchele and Pork", "price" : "one hundred"})
        response = self.app.post('/api/v1/orders', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"price": "kindly provide a price(should be a valid number)"})

    def test_get_one_order(self):
        """Tests successfully getting an order_item through the orders endpoint"""
        response = self.app.get('/api/v1/orders/1')
        self.assertEqual(response.status_code, 200)
    
    def test_getting_non_existing_order(self):
        """Test getting a order_item while providing non-existing id"""
        response = self.app.get('/api/v1/orders/57')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_updating_existing_order(self):
        """Test a successful order item update"""
        data = json.dumps({"order_item" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/orders/1', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_updating_non_existing_order(self):
        """Test updating non_existing order_item"""
        data = json.dumps({"order_item" : "Pilau with spices", "price" : 600})
        response = self.app.put('/api/v1/orders/99', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_successfully_deleting_one_order(self):
        """Test a successful order_item deletion"""
        response = self.app.delete('/api/v1/orders/2')
        self.assertEqual(response.status_code, 200)
    
    def test_deleting_non_existing_order(self):
        """Test a deleting order item that does not exist"""
        response = self.app.delete('/api/v1/orders/15')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
