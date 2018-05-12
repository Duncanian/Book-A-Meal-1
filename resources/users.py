"""Contains all endpoints to manipulate user information
"""
import datetime

from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api, reqparse, inputs, marshal, fields
from werkzeug.security import check_password_hash
import jwt

import models
import config
from .auth import admin_required


user_fields = {
    'id' : fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'admin': fields.Boolean
}


class Signup(Resource):
    "Contains a POST method to register a new user"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            help='kindly provide a valid boolean value',
            type=bool,
            location=['form', 'json'])
        super().__init__()


    def post(self):
        """Register a new user"""
        kwargs = self.reqparse.parse_args()
        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                response = models.User.create_user(
                    username=kwargs.get('username'),
                    email=kwargs.get('email'),
                    password=kwargs.get('password'),
                    admin=False) # you cannot create an admin user through the signup endpoint

                return response
            return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)


class Login(Resource):
    "Contains a POST method to login a user"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        super().__init__()


    def post(self):
        """login a user by providing a token"""
        kwargs = self.reqparse.parse_args()
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = models.User.query.filter_by(email=email).first()

        if user is None: # deliberately ambigous
            return make_response(jsonify({"message" : "invalid email address or password"}), 400)

        if check_password_hash(user.password, password):
            token = jwt.encode({
                'id' : user.id,
                'admin' : user.admin,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(weeks=2)},
                               config.Config.SECRET_KEY)

            return make_response(jsonify({
                "message" : "success, add the token to the header as x-access-token for authentication",
                "token" : token.decode('UTF-8')}), 200)

        return make_response(jsonify({"message" : "invalid email address or password"}), 400)


class UserList(Resource):
    "Contains a POST method to register a new user and a GET method to get all users"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            help='kindly provide a valid boolean value',
            type=bool,
            location=['form', 'json'])
        super().__init__()


    # to be secured in th near future
    def post(self):
        """Create a new user who can have admin privilege"""
        kwargs = self.reqparse.parse_args()
        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                response = models.User.create_user(
                    username=kwargs.get('username'),
                    email=kwargs.get('email'),
                    password=kwargs.get('password'),
                    admin=kwargs.get('admin'))

                return response
            return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)

    @admin_required
    def get(self):
        """Get all users"""
        users = [marshal(user, user_fields) for user in models.User.query.order_by(models.User.id.desc()).all()]
        return make_response(jsonify({'users': users}), 200)


class User(Resource):
    """Contains GET PUT and DELETE methods for interacting with a particular user"""


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='kindly provide a valid username',
            # match anything but newline + something not whitespace + anything but newline
            type=inputs.regex(r"(.*\S.*)"),
            location=['form', 'json']) # the one that comes last is looked at  first
        self.reqparse.add_argument(
            'email',
            required=True,
            help='kindly provide a valid email address',
            location=['form', 'json'],
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='kindly provide a valid confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            required=False,
            nullable=True,
            default=False,
            help='kindly provide a valid boolean value',
            type=bool,
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def get(self, user_id):
        """Get a particular user"""
        response = models.User.get_user(user_id)
        return response

    @admin_required
    def put(self, user_id):
        """Update a particular user"""
        kwargs = self.reqparse.parse_args()
        if kwargs.get('password') == kwargs.get('confirm_password'):
            if len(kwargs.get('password')) >= 8:
                response = models.User.update_user(
                    user_id=user_id,
                    username=kwargs.get('username'),
                    email=kwargs.get('email'),
                    password=kwargs.get('password'),
                    admin=kwargs.get('admin'))
                return response

            return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
        return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)


    @admin_required
    def delete(self, user_id):
        """Delete a particular user"""
        response = models.User.delete_user(user_id)
        return response


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(Signup, '/auth/signup', endpoint='signup')
api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:user_id>', endpoint='user')
