"""Contains all endpoints to manipulate the menu
"""
from flask import jsonify, Blueprint, make_response, request
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal
import jwt

import models
import config
from .auth import token_required, admin_required
from .meals import api

menu_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'price': fields.Integer,
}


class MenuList(Resource):
    """Contains GET and POST methods for manipulating the menu"""
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'meal_id',
            type=int,
            help='kindly provide a valid meal_id',
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Adds a meal to the menu"""
        kwargs = self.reqparse.parse_args()
        meal_id = kwargs.get('meal_id')
        if meal_id:
            response = models.Meal.add_to_menu(meal_id=meal_id)
            return response
        return make_response(jsonify({"message" : "missing meal_id"}), 400)

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


menu_api = Blueprint('resources.menu', __name__)
api = Api(menu_api)

api.add_resource(MenuList, '/menu', endpoint='menus')
api.add_resource(Menu, '/menu/<int:meal_id>', endpoint='menu')
