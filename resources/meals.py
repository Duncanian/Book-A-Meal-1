"""Contains all endpoints to manipulate meal information
"""
from flask import jsonify, Blueprint, make_response
from flask_restful import Resource, Api, reqparse

import data


class MealList(Resource):
    """Contains GET and POST methods"""
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='no name provided',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            help='no price provided',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Adds anew meal option"""
        kwargs = self.reqparse.parse_args()
        for meal_id in data.all_meals:
            if data.all_meals.get(meal_id)["name"] == kwargs.get('name'):
                return jsonify({"message" : "Meal with that name already exists"})

        result = data.Meal.create_meal(**kwargs)
        return make_response(jsonify(result), 201)

    def get(self):
        """Gets all meal options"""
        return make_response(jsonify(data.all_meals), 200)


class Meal(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single meal option"""
    def __init__(self):
        """Validates input given through the form as well as json input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='no name provided',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            help='no price provided',
            location=['form', 'json'])
        super().__init__()

    def get(self, meal_id):
        """Get a particular meal"""
        try:
            meal = data.all_meals[meal_id]
            return make_response(jsonify(meal), 200)
        except KeyError:
            return make_response(jsonify({"message" : "Meal does not exist"}), 404)

    def put(self, meal_id):
        """Update a particular meal"""
        kwargs = self.reqparse.parse_args()
        result = data.Meal.update_meal(meal_id, **kwargs)
        if result != {"message" : "Meal does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

    def delete(self, meal_id):
        """Delete a particular meal"""
        result = data.Meal.delete_meal(meal_id)
        if result != {"message" : "Meal does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

class MenuList(Resource):
    """Contains GET and POST methods for manipulating menu data"""
    def __init__(self):
        """Validates input given through the form as well as json input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='no name provided',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            help='no price provided',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Adds a meal to the menu"""
        kwargs = self.reqparse.parse_args()
        for meal_id in data.all_menu:
            if data.all_menu.get(meal_id)["name"] == kwargs.get('name'):
                return jsonify({"message" : "Meal with that name already exists"})

        result = data.Menu.create_meal(**kwargs)
        return make_response(jsonify(result), 201)


    def get(self):
        """Gets all items on the menu"""
        return make_response(jsonify(data.all_menu), 200)


class Menu(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a singular item on the menu"""
    def __init__(self):
        """Validates input given through the form as well as json input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='no name provided',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            help='no price provided',
            location=['form', 'json'])
        super().__init__()

    def get(self, meal_id):
        """Get a particular meal from the menu"""
        try:
            meal = data.all_menu[meal_id]
            return make_response(jsonify(meal), 200)
        except KeyError:
            return make_response(jsonify({"message" : "Meal does not exist"}), 404)

    def put(self, meal_id):
        """Update a particular meal from the menu"""
        kwargs = self.reqparse.parse_args()
        result = data.Menu.update_meal(meal_id, **kwargs)
        if result != {"message" : "Meal does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

    def delete(self, meal_id):
        """Delete a particular meal from the menu"""
        result = data.Menu.delete_meal(meal_id)
        if result != {"message" : "Meal does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)


class OrderList(Resource):
    """Contains GET and POST methods for manipulating order data"""


    def __init__(self):
        """Validates input given through the form as well as json input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='no name provided',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            help='no price provided',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Creates a new order"""
        kwargs = self.reqparse.parse_args()
        result = data.Order.create_order(**kwargs)
        return make_response(jsonify(result), 201)


    def get(self):
        """Gets all orders"""
        return make_response(jsonify(data.all_orders), 200)


class Order(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""
    def __init__(self):
        """Validates input given through the form as well as json input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='no name provided',
            location=['form', 'json'])
        self.reqparse.add_argument('price',
            required=True,
            help='no price provided',
            location=['form', 'json'])
        super().__init__()

    def get(self, order_id):
        """Get a particular order"""
        try:
            order = data.all_orders[order_id]
            return make_response(jsonify(order), 200)
        except KeyError:
            return make_response(jsonify({"message" : "Order does not exist"}), 404)

    def put(self, order_id):
        """Update a particular order"""
        kwargs = self.reqparse.parse_args()
        result = data.Order.update_order(order_id, **kwargs)
        if result != {"message" : "Order does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

    def delete(self, order_id):
        """Delete a particular order"""
        result = data.Order.delete_order(order_id)
        if result != {"message" : "Order does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)


meals_api = Blueprint('resources.meals', __name__)
api = Api(meals_api) # create the API
api.add_resource(MealList, '/meals', endpoint='meals')
api.add_resource(Meal, '/meals/<int:meal_id>', endpoint='meal')

api.add_resource(MenuList, '/menu', endpoint='menus')
api.add_resource(Menu, '/menu/<int:meal_id>', endpoint='menu')

api.add_resource(OrderList, '/orders', endpoint='orders')
api.add_resource(Order, '/orders/<int:order_id>', endpoint='order')
