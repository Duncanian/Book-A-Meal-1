"""Contains endpoints to manipulate user accounts
"""
import datetime

from flask import Blueprint, jsonify, make_response, request, current_app
from flask_restful import Resource, Api, reqparse, inputs, marshal, fields
from werkzeug.security import check_password_hash
import jwt

import models
import config
from .auth import token_required


class Signup(Resource):
    "Contains a POST method to register a new user"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='missing username',
            location=['form', 'json']) # the one that comes last is looked at  first
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
        super().__init__()

    def post(self):
        """Register a new user"""
        kwargs = self.reqparse.parse_args()
        username =  kwargs.get('username').lstrip().rstrip()
        email =  kwargs.get('email')
        password =  kwargs.get('password')
        confirm_password =  kwargs.get('confirm_password')

        if username:
            if email:
                if password == confirm_password:
                    if len(password) >= 8:
                        response = models.User.create_user(
                            username=username,
                            email=email,
                            password=password,
                            admin=False) # all users created through the signup endpoint are non-admins

                        return response
                    return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
                return make_response(jsonify({"message" : "password and confirm password should be identical"}), 400)
            return make_response(jsonify({"message" : "missing email address"}), 400)
        return make_response(jsonify({"message" : "kindly provide a valid username"}), 400)


class Login(Resource):
    "Contains a POST method to login a user"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
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
        super().__init__()

    def post(self):
        """login a user by providing a token"""
        kwargs = self.reqparse.parse_args()
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = models.User.query.filter_by(email=email).first()

        if not email:
            return make_response(jsonify({"message" : "missing email address"}), 400)

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


class ResetPassword(Resource):
    "Contains a POST method to reset your password"


    def __init__(self):
        """Validates both json and form-data input"""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'current_password',
            required=True,
            trim=True,
            help='missing current password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'new_password',
            required=True,
            trim=True,
            help='missing new password',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'confirm_password',
            required=True,
            trim=True,
            help='missing confirmation password',
            location=['form', 'json'])
        super().__init__()

    @token_required
    def post(self):
        """Reset user's password"""
        kwargs = self.reqparse.parse_args()
        current_password = kwargs.get('current_password')
        new_password = kwargs.get('new_password')
        confirm_password = kwargs.get('confirm_password')
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']
        user = models.User.query.get(user_id)

        if check_password_hash(user.password, current_password):
            if current_password != new_password:
                if new_password == confirm_password:
                    if len(new_password) >= 8:
                        response = models.User.reset_password(
                            user_id=user.id,
                            password=new_password)

                        return response
                    return make_response(jsonify({"message" : "password should be at least 8 characters"}), 400)
                return make_response(jsonify({"message" : "new password and confirm password should be identical"}), 400)
            return make_response(jsonify({"message" : "current password and new password are identical"}), 400)
        return make_response(jsonify({"message" : "invalid password"}), 400)


class TestAdmin(Resource):
    "Contains a GET method to setup an admin to be used for testing"


    def get(self):
        """Create admin user to be used in tests. Wil run only when TESTING is True"""
        if current_app.config['TESTING']:
            response = models.User.create_user(
                username="admin",
                email="admin@gmail.com",
                password="12345678",
                admin=True)
            return response


account_api = Blueprint('resources.account', __name__)
api = Api(account_api)

api.add_resource(Signup, '/auth/signup', endpoint='signup')
api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(ResetPassword, '/auth/reset', endpoint='reset')
api.add_resource(TestAdmin, '/create_test_admin', endpoint='create_test_admin')
