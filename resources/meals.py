
# testing responses using postman
from flask import jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse


class MealList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='No meal name provided',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            help='No meal price provided',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        kwargs = self.reqparse.parse_args()
        return jsonify({"message" : "Meal option created successfully",
                        "new_meal_option" : {1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}}})

    def get(self):
        return jsonify({1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450},
                        2: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450},
                        3: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}})


class Meal(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',
            required=True,
            help='No course name provided',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument('price',
            required=True,
            help='No course price provided',
            location=['form', 'json'])
        super().__init__()

    def get(self, meal_id):
        return jsonify({1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}})

    def put(self, meal_id):
        kwargs = self.reqparse.parse_args()
        return jsonify({"message" : "Account updated successfully",
                        "updated meal" : {1: {"meal_id" : 1, "name" : "Rice and Beef"}}})

    def delete(self, meal_id):
        return jsonify({"message" : "Meal deleted successfully"})

class MenuList(Resource):


    def get(self):
        return jsonify({1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450},
                        2: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450},
                        3: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}})

class Menu(Resource):
    

    def get(self, meal_id):
        return jsonify({1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}})

    def put(self, meal_id):
        return jsonify({"message" : "Account added to menu successfully",
                        "meal_added_to_menu" : {1: {"meal_id" : 1, "name" : "Rice and Beef"}}})

    def delete(self, meal_id):
        return jsonify({"message" : "Meal deleted from menu successfully"})

class OrderList(Resource):


    def get(self):
        return jsonify({1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450, "user_id" : 1, "username " : "lenny", },
                        2: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450},
                        3: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}})

class Menu(Resource):
    

    def get(self, meal_id):
        return jsonify({1: {"meal_id" : 1, "name" : "Rice and Beans", "price" : 450}})

    def put(self, meal_id):
        return jsonify({"message" : "Account added to menu successfully",
                        "meal_added_to_menu" : {1: {"meal_id" : 1, "name" : "Rice and Beef"}}})

    def delete(self, meal_id):
        return jsonify({"message" : "Meal deleted from menu successfully"})
meals_api = Blueprint('resources.meals', __name__)

# create the API
api = Api(meals_api)
api.add_resource(MealList, '/meals', endpoint='meals')
api.add_resource(Meal, '/meals/<int:meal_id>', endpoint='meal')

api.add_resource(MenuList, '/menus', endpoint='menus')
api.add_resource(Menu, '/menus/<int:meal_id>', endpoint='menu')
