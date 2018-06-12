"""Contains all endpoints to manipulate user information
"""
import datetime

from flask import Blueprint, jsonify, make_response, request, current_app
from flask_restful import Resource, Api, reqparse, inputs, marshal, fields
from werkzeug.security import check_password_hash
import jwt

import models
import config
from .auth import admin_required, token_required


user_fields = {
    'id' : fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'admin': fields.Boolean,
    'orders' : fields.List(fields.String) # list of strings
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
                    admin=False) # all users created through the signup endpoint are non-admins

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
            type=inputs.boolean,
            location=['form', 'json'])
        super().__init__()

    @admin_required
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
            type=inputs.boolean,
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


    @token_required
    def delete(self, user_id):
        """Delete a particular user"""
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        admin = data['admin']
        token_user_id = data['id']
        user = models.User.query.get(user_id)

        if admin or user.id == token_user_id:
            response = models.User.delete_user(user_id)
            return response

        return make_response(jsonify({
            "message" : "sorry, you cannot delete this account since it does not belong to you"}), 401)


class ResetPassword(Resource):
    "Contains a POST method to reset your password"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'current_password',
            required=True,
            trim=True,
            help='kindly provide a valid password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'new_password',
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
        super().__init__()

    @token_required
    def post(self):
        """Reset user's password"""
        kwargs = self.reqparse.parse_args()
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']
        user = models.User.query.get(user_id)

        if check_password_hash(user.password, kwargs.get('current_password')):
            if kwargs.get('current_password') != kwargs.get('new_password'):
                if kwargs.get('new_password') == kwargs.get('confirm_password'):
                    if len(kwargs.get('new_password')) >= 8:
                        response = models.User.reset_password(
                            user_id=user.id,
                            password=kwargs.get('new_password'))

                        return response
                    return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
                return make_response(jsonify({"message" : "new password and confirm password should be identical"}), 400)
            return make_response(jsonify({"message" : "current password and new password are identical"}), 400)
        return make_response(jsonify({"message" : "invalid password"}), 400)


class TestAdmin(Resource):
    def get(self):
        """Create admin user to be used in tests. Wil run only when TESTING is True"""
        if current_app.config['TESTING']:
            response = models.User.create_user(
                username="admin",
                email="admin@gmail.com",
                password="12345678",
                admin=True)
            return response


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(Signup, '/auth/signup', endpoint='signup')
api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:user_id>', endpoint='user')
api.add_resource(ResetPassword, '/auth/reset', endpoint='reset')
api.add_resource(TestAdmin, '/create_test_admin', endpoint='create_test_admin')
