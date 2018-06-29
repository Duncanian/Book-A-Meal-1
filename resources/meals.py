"""Contains all endpoints to manipulate meals
"""
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


class MealList(Resource):
    """Contains GET and POST methods for manipulating meal information"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='missing name',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            type=int,
            trim=True,
            help='kindly provide a valid integer as the price',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'in_menu',
            type=inputs.boolean,
            trim=True,
            help='kindly provide a valid boolean as the in_menu value',
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Adds a new meal"""
        kwargs = self.reqparse.parse_args()
        name =  kwargs.get('name').lstrip().rstrip()
        price =  kwargs.get('price')
        in_menu =  kwargs.get('in_menu')

        if name:
            if price:
                if in_menu == True or in_menu == False: # catches no input provided without letting in invalid input
                    response = models.Meal.create_meal(
                        name=name,
                        price=price,
                        in_menu=in_menu)
                    return response
                return make_response(jsonify({"message" : "missing in_menu value"}), 400)    
            return make_response(jsonify({"message" : "missing  price"}), 400)
        return make_response(jsonify({"message" : "kindly provide a valid name"}), 400)
        

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
            help='missing name',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'price',
            type=int,
            trim=True,
            help='kindly provide a valid integer as the price',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'in_menu',
            type=inputs.boolean,
            trim=True,
            help='kindly provide a valid boolean as the in_menu value',
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
        name =  kwargs.get('name').lstrip().rstrip()
        price =  kwargs.get('price')
        in_menu =  kwargs.get('in_menu')

        if name:
            if price:
                if in_menu == True or in_menu == False:
                    response = models.Meal.update_meal(
                        meal_id=meal_id,
                        name=name,
                        price=price,
                        in_menu=in_menu)
                    return response
                return make_response(jsonify({"message" : "missing in_menu value"}), 400)    
            return make_response(jsonify({"message" : "missing  price"}), 400)
        return make_response(jsonify({"message" : "kindly provide a valid name"}), 400)

    @admin_required
    def delete(self, meal_id):
        """Delete a particular meal"""
        response = models.Meal.delete_meal(meal_id)
        return response


meals_api = Blueprint('resources.meals', __name__)
api = Api(meals_api)

api.add_resource(MealList, '/meals', endpoint='meals')
api.add_resource(Meal, '/meals/<int:meal_id>', endpoint='meal')
