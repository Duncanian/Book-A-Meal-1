"""Tests the reset password endpoint on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class ResetTests(BaseTests):
    """Test functionality of the reset password endpoint"""


    def test_good_reset(self):
        """Test successfully resettng password"""
        data = json.dumps({
            "current_password" : "12345678", "new_password" : "secret12345",
            "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_signup_wrong_password(self):
        """Test unsuccessful reset because of wrong current password"""
        data = json.dumps({
            "current_password" : "5512345678", "new_password" : "secret12345",
            "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_signup_unmatching_password(self):
        """Test unsuccessful reset because of wrong current password"""
        data = json.dumps({
            "current_password" : "12345678", "new_password" : "secret12345",
            "confirm_password" : "secret123456"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_signup_short_passwords(self):
        """Test unsuccessful reset because of short passwords"""
        data = json.dumps({
            "current_password" : "12345678", "new_password" : "1234567",
            "confirm_password" : "1234567"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_signup_same_password(self):
        """Test unsuccessful reset because of short passwords"""
        data = json.dumps({
            "current_password" : "12345678", "new_password" : "12345678",
            "confirm_password" : "12345678"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_current(self):
        """Test unsuccessfully reset because of empty current password"""
        data = json.dumps({
            "current_password" : "", "new_password" : "secret12345",
            "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_new(self):
        """Test unsuccessfully reset because of empty new password"""
        data = json.dumps({
            "current_password" : "12345678", "new_password" : "",
            "confirm_password" : "secret12345"})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)

    def test_empty_confirm(self):
        """Test unsuccessfully reset because of empty confirm password"""
        data = json.dumps({
            "current_password" : "12345678", "new_password" : "secret12345",
            "confirm_password" : ""})
        response = self.app.post(
            '/api/v3/auth/reset', data=data,
            content_type='application/json',
            headers=self.user_header)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
