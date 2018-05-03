"""Contains the decorator that checks that the user has a token in the request header.
We get access to the user's credentials by decoding a token from a particular token
"""
from functools import wraps

from flask import Flask, request, jsonify, make_response
import jwt

import config
import models

def token_required(f):
    """gets token from header and returns the user id"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if token is None:
            return make_response(jsonify({"message" : "kindly provide a valid token in the request header"}), 401)

        try: 
            data = jwt.decode(token, config.Config.SECRET_KEY)
        except:
            return make_response(jsonify({"message" : "kindly provide a valid token in the request header"}), 401)
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """gets token from header ensures that the user is an admin and returns the user id"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if token is None:
            return make_response(jsonify({"message" : "kindly provide a valid token in the request header"}), 401)

        try: 
            data = jwt.decode(token, config.Config.SECRET_KEY)
            admin = data['admin']
        except:
            return make_response(jsonify({"message" : "kindly provide a valid token in the request header"}), 401)

        if not admin:
            return make_response(jsonify({"message" : "you are not authorized to perform this function as a non-admin user"}), 401)
        
        return f(*args, **kwargs)

    return decorated
