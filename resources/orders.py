"""Contains endpoints to manipulate orders
"""
from flask import jsonify, Blueprint, make_response, request
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal
import jwt

import models
import config
from .auth import token_required, admin_required
from .meals import api

order_fields = {
    'id' : fields.Integer,
    'meal_id': fields.Integer,
    'meal_name': fields.String,
    'price': fields.Integer,
    'user_id' : fields.Integer,
    'user_email' : fields.String,
    'created_at' : fields.DateTime
}


class OrderList(Resource):
    """Contains GET and POST methods for manipulating orders"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_id',
            type=int,
            help='kindly provide a valid meal_id',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def post(self):
        """Creates a new order"""
        kwargs = self.reqparse.parse_args()
        meal_id = kwargs.get('meal_id')
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']

        if meal_id:
            response = models.Order.create_order(user_id=user_id, meal_id=meal_id)
            return response
        return make_response(jsonify({"message" : "missing meal_id"}), 400)

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
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_id',
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
                "message" : "order does not belong to you"}), 404)

        return response

    @token_required
    def put(self, order_id):
        """Update a particular order"""
        kwargs = self.reqparse.parse_args()
        meal_id = kwargs.get('meal_id')
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        user_id = data['id']
        order = models.Order.query.get(order_id)

        if not meal_id:
            return make_response(jsonify({"message" : "missing meal_id"}), 400)

        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)

        if admin or order.user_id == user_id:
            response = models.Order.update_order(
                order_id=order_id, meal_id=meal_id)
            return response

        return make_response(jsonify({
            "message" : "order does not belong to you"}), 401)

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
                "message" : "order does not belong to you"}), 401)


orders_api = Blueprint('resources.orders', __name__)
api = Api(orders_api)

api.add_resource(OrderList, '/orders', endpoint='orders')
api.add_resource(Order, '/orders/<int:order_id>', endpoint='order')
