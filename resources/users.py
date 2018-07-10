"""Contains endpoints to manipulate users
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


class UserList(Resource):
    "Contains a POST method to register a new user and a GET method to get all users"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            trim=True,
            help='missing username',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
            trim=True,
            help='kindly provide a valid email address',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='missing password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='missing confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            default=False,
            help='kindly provide a valid boolean as the admin value',
            type=inputs.boolean,
            location=['form', 'json'])
        super().__init__()

    @admin_required
    def post(self):
        """Create a new user who can have admin privilege"""
        kwargs = self.reqparse.parse_args()
        username =  kwargs.get('username').lstrip().rstrip()
        email =  kwargs.get('email')
        password =  kwargs.get('password')
        confirm_password =  kwargs.get('confirm_password')
        admin = kwargs.get('admin')

        if username:
            if email:
                if password == confirm_password:
                    if len(password) >= 8:
                        response = models.User.create_user(
                            username=username,
                            email=email,
                            password=password,
                            admin=admin)

                        return response
                    return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
                return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)
            return make_response(jsonify({"message" : "missing email address"}), 400)
        return make_response(jsonify({"message" : "kindly provide a valid username"}), 400)

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
            trim=True,
            help='missing username',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'email',
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
            trim=True,
            help='kindly provide a valid email address',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'password',
            required=True,
            trim=True,
            help='missing password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='missing confirmation password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'admin',
            default=False,
            help='kindly provide a valid boolean as the admin value',
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
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')
        confirm_password = kwargs.get('confirm_password')
        admin = kwargs.get('admin')

        if username:
            if email:
                if password == confirm_password:
                    if len(password) >= 8:
                        response = models.User.update_user(
                            user_id=user_id,
                            username=username,
                            email=email,
                            password=password,
                            admin=admin)

                        return response
                    return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
                return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)
            return make_response(jsonify({"message" : "missing email address"}), 400)
        return make_response(jsonify({"message" : "kindly provide a valid username"}), 400)

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


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:user_id>', endpoint='user')
