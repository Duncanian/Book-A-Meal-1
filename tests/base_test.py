"""Authenticate a user and an admin to be used during testing
Set up required items to be used during testing
"""
# pylint: disable=W0612
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
import app



class BaseTests(unittest.TestCase):
    """Authenticate a user and an admin and make the tokens available.
    Create a meal and menu option and also create an order
    """


    def setUp(self):
        """Authenticate a user and an admin and make the tokens available"""
        self.application = app.create_app('config.TestingConfig')

        admin_reg = json.dumps({
            "username" : "admin",
            "email" : "admin@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678",
            "admin" : True})

        user_reg = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678"})

        admin_log = json.dumps({
            "email" : "admin@gmail.com",
            "password" : "12345678"})

        user_log = json.dumps({
            "email" : "user@gmail.com",
            "password" : "12345678"})

        self.app = self.application.test_client()

        with self.application.app_context():
            models.db.create_all()

            create_admin = self.app.post(
                '/api/v3/users', data=admin_reg,
                content_type='application/json')
            admin_result = self.app.post(
                '/api/v3/auth/login', data=admin_log,
                content_type='application/json')
            register_user = self.app.post(
                '/api/v3/auth/signup', data=user_reg,
                content_type='application/json')
            user_result = self.app.post(
                '/api/v3/auth/login', data=user_log,
                content_type='application/json')
            user_response = json.loads(user_result.get_data(as_text=True))
            user_token = user_response["token"]
            self.user_header = {"Content-Type" : "application/json", "x-access-token" : user_token}

            admin_response = json.loads(admin_result.get_data(as_text=True))
            admin_token = admin_response["token"]
            self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}

            meal = json.dumps({"name" : "ugali", "price" : "20", "in_menu" : False})
            menu = json.dumps({"name" : "chapo", "price" : "20", "in_menu" : True})
            order = json.dumps({"meal_id" : 2})
            create_meal = self.app.post(
                '/api/v3/meals', data=meal, content_type='application/json',
                headers=self.admin_header)
            create_menu = self.app.post(
                '/api/v3/meals', data=menu, content_type='application/json',
                headers=self.admin_header)
            make_order = self.app.post(
                '/api/v3/orders', data=order,
                content_type='application/json',
                headers=self.user_header)

    def tearDown(self):
        with self.application.app_context():
            models.db.session.remove()
            models.db.drop_all()
