"""Contains all endpoints to manipulate meals, menu and orders information
"""
import datetime

from flask import jsonify, Blueprint, make_response, request
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal
import jwt

import models
import config
from .auth import token_required, admin_required

meal_fields = {
    'id' : fields.Integer,
    'meal_item': fields.String,
    'price': fields.Integer,
}

menu_fields = {
    'id' : fields.Integer,
    'menu_option': fields.String,
    'price': fields.Integer,
}

order_fields = {
    'id' : fields.Integer,
    'order_item': fields.String,
    'price': fields.Integer,
    'client_id' : fields.Integer,
    'client_email' : fields.String,
    'created_at' : fields.DateTime
}


class MealList(Resource):
    """Contains GET and POST methods for manipulating meal information"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a meal item',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            required=True,
            type=int,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Adds a new meal item"""
        kwargs = self.reqparse.parse_args()
        response = models.Meal.create_meal(
            meal_item=kwargs.get('meal_item'),
            price=kwargs.get('price'))
        return response

    @admin_required
    def get(self):
        """Gets all meal items"""
        meals = [marshal(meal, meal_fields) for meal in models.Meal.query.order_by(models.Meal.id.desc()).all()]  
        return make_response(jsonify({'meals': meals}), 200)


class Meal(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single meal option"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a meal item',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            required=True,
            type=int,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def get(self, meal_id):
        """Get a particular meal"""
        response = models.Meal.get_meal(meal_id)
        return response

    @admin_required
    def put(self, meal_id):
        """Update a particular meal"""
        kwargs = self.reqparse.parse_args()
        response = models.Meal.update_meal(
            meal_id=meal_id,
            meal_item=kwargs.get('meal_item'),
            price=kwargs.get('price'))
        return response

    @admin_required
    def delete(self, meal_id):
        """Delete a particular meal"""
        response = models.Meal.delete_meal(meal_id)
        return response

class MenuList(Resource):
    """Contains GET and POST methods for manipulating menu data"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'menu_option',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a menu option',
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Adds a menu option to the menu"""
        kwargs = self.reqparse.parse_args()
        response = models.Menu.create_menu(
            menu_option=kwargs.get('menu_option'))
        return response

    @token_required
    def get(self):
        """Gets all menu options on the menu"""
        menus = [marshal(menu, menu_fields) for menu in models.Menu.query.order_by(models.Menu.id.desc()).all()]  
        return make_response(jsonify({'menu': menus}), 200)


class Menu(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single menu option"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'menu_option',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a menu option',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def get(self, menu_id):
        """Get a particular menu option"""
        response = models.Menu.get_menu(menu_id)
        return response

    @admin_required
    def put(self, menu_id):
        """Update a particular menu option"""
        kwargs = self.reqparse.parse_args()
        response = models.Menu.update_menu(
            menu_id=menu_id,
            menu_option=kwargs.get('menu_option'))
        return response

    @admin_required
    def delete(self, menu_id):
        """Delete a particular menu option"""
        response = models.Menu.delete_menu(menu_id)
        return response


class OrderList(Resource):
    """Contains GET and POST methods for manipulating orders"""


    def __init__(self):
        self.now = datetime.datetime.utcnow() # timer
        self.closing = datetime.time(23, 0, 0)

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'order_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide an order item',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def post(self):
        """Creates a new order"""
        kwargs = self.reqparse.parse_args()
        if self.now.hour < self.closing.hour:
            token = request.headers['x-access-token']
            data = jwt.decode(token, config.Config.SECRET_KEY)
            user_id = data['id']
            client = models.User.query.get(user_id)
            response = models.Order.create_order(
                order_item=kwargs.get('order_item'),
                client_id=client.id,
                client_email=client.email)
            return response
        return make_response(jsonify({"message" : "sorry, we do not take orders past 11PM"}), 200)


    @token_required
    def get(self):
        """Gets all orders for admin and get all orders belonging to the current authenticated user"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        user_orders = [marshal(order, order_fields) for order in models.Order.query.filter_by(client_id=user_id).all()]

        if admin:
            orders = [marshal(order, order_fields) for order in models.Order.query.order_by(models.Order.id.desc()).all()]  
            return make_response(jsonify({'orders': orders}), 200)
        return make_response(jsonify({'your orders': user_orders}), 200)


class Order(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single order"""


    def __init__(self):
        self.now = datetime.datetime.utcnow() # timer
        self.closing = datetime.time(23, 0, 0)

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'order_item',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide an order item',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def get(self, order_id):
        """Get a particular order"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        order = models.Order.query.filter_by(client_id=user_id, id=order_id).first()
        response = models.Order.get_order(order_id)

        if admin:
            return response
        
        if order is None:
            return make_response(jsonify({"message" : "order does not exists or it does not belong to you"}), 404)
        return response


    @token_required
    def put(self, order_id):
        """Update a particular order"""
        if self.now.hour < self.closing.hour:
            kwargs = self.reqparse.parse_args()
            token = request.headers['x-access-token']
            data = jwt.decode(token, config.Config.SECRET_KEY)
            admin = data['admin']
            user_id = data['id']
            order = models.Order.query.get(order_id)

            if admin or order.client_id == user_id:
                response = models.Order.update_order(
                    order_id=order_id, order_item=kwargs.get('order_item'))
                return response
            return make_response(jsonify({
                "message" : "sorry, you cannot update this order since it does not belong to you"}), 401)
        return make_response(jsonify({"message" : "sorry, we do not take orders past 11PM"}), 200)
        

    @token_required
    def delete(self, order_id):
        """Delete a particular order"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        order = models.Order.query.get(order_id)

        if admin or order.client_id == user_id:
            response = models.Order.delete_order(order_id)
            return response
        return make_response(jsonify({
                "message" : "sorry, you cannot delete this order since it does not belong to you"}), 401)


meals_api = Blueprint('resources.meals', __name__)
api = Api(meals_api) # create the API
api.add_resource(MealList, '/meals', endpoint='meals')
api.add_resource(Meal, '/meals/<int:meal_id>', endpoint='meal')

api.add_resource(MenuList, '/menu', endpoint='menus')
api.add_resource(Menu, '/menu/<int:menu_id>', endpoint='menu')

api.add_resource(OrderList, '/orders', endpoint='orders')
api.add_resource(Order, '/orders/<int:order_id>', endpoint='order')
