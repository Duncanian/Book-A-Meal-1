"""Contains all endpoints to manipulate user information
"""

from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse, inputs

import data


class UserList(Resource):
    "Contains a POST method to register a new user and a GET method to get all users"


    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='no username provided',
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='no email provided',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            help='no password provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            help='no password confirmation provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            location=['form', 'json'])
        super().__init__()

    def post(self):
        """Register a new user"""
        kwargs = self.reqparse.parse_args()
        for user_id in data.all_users:
            if data.all_users.get(user_id)["email"] == kwargs.get('email'):
                return jsonify({"message" : "User with that email already exists"})

        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                result = data.User.create_user(**kwargs)
                return make_response(jsonify(result), 201)
            return jsonify({"message" : "Password should be at least 8 characters"})
        return jsonify({"message" : "Password and confirm_password should be identical"})

    def get(self):
        """Get all users"""
        return make_response(jsonify(data.all_users), 200)


class User(Resource):
    def __init__(self):
        "Validates input from the form as well as json input"
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='no username provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            required=True,
            help='no email provided',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            help='no password provided',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            help='no password confirmation provided',
            location=['form', 'json'])
        super().__init__()


    def get(self, user_id):
        """Get a particular user"""
        try:
            user = data.all_users[user_id]
            return make_response(jsonify(user), 200)
        except KeyError:
            return make_response(jsonify({"message" : "User does not exist"}), 404)

    def put(self, user_id):
        """Update a particular user"""
        kwargs = self.reqparse.parse_args()
        result = data.User.update_user(user_id, **kwargs)
        if result != {"message" : "User does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)

    def delete(self, user_id):
        """Delete a particular user"""
        result = data.User.delete_user(user_id)
        if result != {"message" : "User does not exist"}:
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify(result), 404)



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(UserList, '/auth/signup', endpoint='users')
api.add_resource(User, '/users/<int:user_id>', endpoint='user')
