"""Authenticate a user and an admin to be used during testing
"""
# pylint: disable=W0612
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app
import models

db = models.db


class BaseTests(unittest.TestCase):
    """Authenticate a user and an admin and make the tokens available"""


    def setUp(self):
        """Authenticate a user and an admin and make the tokens available"""
        self.application = app.create_app('config.TestingConfig')
        self.user_reg = json.dumps({
            "username" : "user",
            "email" : "user@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678"})
        
        self.admin_reg = json.dumps({
            "username" : "admin",
            "email" : "admin@gmail.com",
            "password" : "12345678",
            "confirm_password" : "12345678",
            "admin" : True})

        self.user_log = json.dumps({
            "email" : "user@gmail.com",
            "password" : "12345678"})
        
        self.admin_log = json.dumps({
             "email" : "admin@gmail.com",
            "password" : "12345678"})

        self.app = self.application.test_client()
        
        with self.application.app_context():
            db.create_all()
            register_user = self.app.post(
                '/api/v2/auth/signup', data=self.user_reg,
                content_type='application/json')
            register_admin = self.app.post(
                '/api/v2/auth/signup', data=self.admin_reg,
                content_type='application/json')
            user_result = self.app.post(
                '/api/v2/auth/login', data=self.user_log,
                content_type='application/json')
            admin_result = self.app.post(
                '/api/v2/auth/login', data=self.admin_log,
                content_type='application/json')
            user_response = json.loads(user_result.get_data(as_text=True))
            user_token = user_response["token"]
            self.user_header = {"Content-Type" : "application/json", "x-access-token" : user_token}

            admin_response = json.loads(admin_result.get_data(as_text=True))
            admin_token = admin_response["token"]
            self.admin_header = {"Content-Type" : "application/json", "x-access-token" : admin_token}

    def tearDown(self):
        with self.application.app_context():
            db.session.remove()
            db.drop_all()
