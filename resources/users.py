"""Contains all endpoints to manipulate user data

Created: April 2018
Author: Lenny
"""

from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse, inputs

import data


class UserList(Resource):
    "Contains a POST method to create a new user and a GET method to get all users"


    def __init__(self):
        "Validates input both from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No Username Provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email Provided',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No Password Provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            help='No Password Confirmation Provided',
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Create a new user"""
        kwargs = self.reqparse.parse_args()
        result = data.User.create_user(**kwargs)
        return make_response(jsonify(result), 201)

    def get(self):
        """Get all users"""
        return make_response(jsonify(data.all_users), 200)


# testing responses using Postman
class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email Provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No Username Provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No Password Provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            help='No Password Confirmation Provided',
            location=['form', 'json'])
        super().__init__()


    def get(self, user_id):
        return jsonify({1: {"user_id" : 1, "email" : "lennykmutua@gmail.com", "username" : "lenny",
                        "password" : "secret"}})

    def put(self, user_id):
        kwargs = self.reqparse.parse_args()
        return jsonify({"message" : "Account updated successfully",
                        "updated_user" : {1: {"user_id" : 1, "email" : "lennykmutua@gmail.com", "username" : "lenny",
                        "password" : "secret"}}})

    def delete(self, user_id):
        return jsonify({"message" : "User deleted successfully"})



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:user_id>', endpoint='user')
