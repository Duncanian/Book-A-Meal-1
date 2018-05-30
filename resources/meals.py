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
    'name': fields.String,
    'price': fields.Integer,
    'in_menu': fields.Boolean
}

menu_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'price': fields.Integer,
}

order_fields = {
    'id' : fields.Integer,
    'meal_id': fields.Integer,
    'meal_name': fields.String,
    'price': fields.Integer,
    'user_id' : fields.Integer,
    'user_email' : fields.String,
    'created_at' : fields.DateTime
}


class MealList(Resource):
    """Contains GET and POST methods for manipulating meal information"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a valid name',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            required=True,
            type=int,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'in_menu',
            required=True,
            help='kindly provide a valid boolean value',
            type=inputs.boolean,
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Adds a new meal"""
        kwargs = self.reqparse.parse_args()
        response = models.Meal.create_meal(
            name=kwargs.get('name'),
            price=kwargs.get('price'),
            in_menu=kwargs.get('in_menu'))
        return response

    @admin_required
    def get(self):
        """Gets all meals"""
        meals = [marshal(meal, meal_fields) for meal in models.Meal.query.order_by(models.Meal.id.desc()).all()]
        return make_response(jsonify({'meals': meals}), 200)


class Meal(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single meal option"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a valid name',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            required=True,
            type=int,
            help='kindly provide a price(should be a valid number)',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'in_menu',
            required=True,
            help='kindly provide a valid boolean value',
            type=inputs.boolean,
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
            name=kwargs.get('name'),
            price=kwargs.get('price'),
            in_menu=kwargs.get('in_menu'))
        return response

    @admin_required
    def delete(self, meal_id):
        """Delete a particular meal"""
        response = models.Meal.delete_meal(meal_id)
        return response


class MenuList(Resource):
    """Contains GET and POST methods for manipulating the menu"""
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_id',
            required=True,
            type=int,
            help='kindly provide a valid meal_id',
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Adds a meal to the menu"""
        kwargs = self.reqparse.parse_args()
        response = models.Meal.add_to_menu(meal_id=kwargs.get('meal_id'))
        return response

    @token_required
    def get(self):
        """Gets all meals on the menu"""
        menus = [marshal(menu, menu_fields) for menu in models.Meal.query.filter_by(in_menu=True).all()]
        return make_response(jsonify({'menu': menus}), 200)


class Menu(Resource):
    """Contains GET and delete methods for manipulating a menu item"""


    @token_required
    def get(self, meal_id):
        """Get a particular meal on the menu"""
        response = models.Meal.get_menu(meal_id)
        return response

    @admin_required
    def delete(self, meal_id):
        """Remove a particular meal from the menu"""
        response = models.Meal.remove_from_menu(meal_id)
        return response



class OrderList(Resource):
    """Contains GET and POST methods for manipulating orders"""


    def __init__(self):
        self.now = datetime.datetime.utcnow().hour
        self.opening = datetime.time(8, 0, 0).hour
        self.closing = datetime.time(20, 0, 0).hour

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_id',
            required=True,
            type=int,
            help='kindly provide a valid meal_id',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def post(self):
        """Creates a new order"""
        kwargs = self.reqparse.parse_args()
        if self.opening < self.now < self.closing:
            token = request.headers['x-access-token']
            data = jwt.decode(token, config.Config.SECRET_KEY)
            user_id = data['id']
            response = models.Order.create_order(user_id=user_id, meal_id=kwargs.get('meal_id'))
            return response

        return make_response(jsonify({"message" : "sorry, we are only open between 8AM and 8PM"}), 200)


    @token_required
    def get(self):
        """Gets all orders for admin and get all orders belonging to the current authenticated user"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        user_orders = [marshal(order, order_fields) for order in models.Order.query.filter_by(user_id=user_id).all()]

        if admin:
            orders = [marshal(order, order_fields) for order in models.Order.query.order_by(models.Order.id.desc()).all()]
            return make_response(jsonify({'orders': orders}), 200)

        return make_response(jsonify({'your orders': user_orders}), 200)


class Order(Resource):
    """Contains GET, PUT and DELETE methods for manipulating an order"""


    def __init__(self):
        self.now = datetime.datetime.utcnow().hour
        self.opening = datetime.time(8, 0, 0).hour
        self.closing = datetime.time(20, 0, 0).hour

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_id',
            required=True,
            type=int,
            help='kindly provide a valid meal_id',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def get(self, order_id):
        """Get a particular order"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        order = models.Order.query.filter_by(user_id=user_id, id=order_id).first()
        response = models.Order.get_order(order_id)

        if admin:
            return response

        if order is None:
            return make_response(jsonify({
                "message" : "order does not exists or it does not belong to you"}), 404)

        if response is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)

        return response

    @token_required
    def put(self, order_id):
        """Update a particular order"""
        if self.opening < self.now < self.closing:
            kwargs = self.reqparse.parse_args()
            token = request.headers['x-access-token']
            data = jwt.decode(token, config.Config.SECRET_KEY)
            admin = data['admin']
            user_id = data['id']
            order = models.Order.query.get(order_id)

            if order is None:
                return make_response(jsonify({"message" : "order does not exists"}), 404)

            if admin or order.user_id == user_id:
                response = models.Order.update_order(
                    order_id=order_id, meal_id=kwargs.get('meal_id'))
                return response

            return make_response(jsonify({
                "message" : "sorry, you cannot update this order since it does not belong to you"}), 401)

        return make_response(jsonify({"message" : "sorry, we are only open between 8AM and 8PM"}), 200)


    @token_required
    def delete(self, order_id):
        """Delete a particular order"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        order = models.Order.query.get(order_id)

        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)

        if admin or order.user_id == user_id:
            response = models.Order.delete_order(order_id)
            return response
        return make_response(jsonify({
                "message" : "sorry, you cannot delete this order since it does not belong to you"}), 401)


meals_api = Blueprint('resources.meals', __name__)
api = Api(meals_api) # create the API
api.add_resource(MealList, '/meals', endpoint='meals')
api.add_resource(Meal, '/meals/<int:meal_id>', endpoint='meal')

api.add_resource(MenuList, '/menu', endpoint='menus')
api.add_resource(Menu, '/menu/<int:meal_id>', endpoint='menu')

api.add_resource(OrderList, '/orders', endpoint='orders')
api.add_resource(Order, '/orders/<int:order_id>', endpoint='order')
