"""Handles data storage for Users, Meals, Menu and Orders
"""
# pylint: disable=E1101
import datetime

from flask import make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Contains user columns and methods to add, update and delete a user"""


    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean)
    orders = db.relationship('Order', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<user {}>'.format(self.username)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        """Creates a new user and ensures that the email is unique"""

        by_email = cls.query.filter_by(email=email).first()

        if by_email is None:
            password = generate_password_hash(password, method='sha256')
            new_user = cls(username=username, email=email, password=password, admin=admin)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({
                "message" : "user has been successfully created",
                str(new_user.id) : {"username" : new_user.username,
                                    "email" : new_user.email,
                                    "admin" : new_user.admin}}), 201)


        return make_response(jsonify({"message" : "user with that email already exists"}), 400)

    @staticmethod
    def update_user(user_id, username, email, password, admin):
        """Updates user information"""
        user = User.query.get(user_id)
        by_email = User.query.filter_by(email=email).first()

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        if user.username == username and user.email == email and user.admin == admin and check_password_hash(user.password, password):
            return make_response(jsonify({"message" : "No changes detected"}), 400)

        if by_email is None or by_email.id == user.id:
            user.username = username
            user.email = email
            user.password = generate_password_hash(password, method='sha256')
            user.admin = admin
            db.session.commit()
            return make_response(jsonify({
                "message" : "user has been successfully updated",
                str(user.id) : {"username" : user.username,
                                "email" : user.email,
                                "admin" : user.admin}}), 200)

        return make_response(jsonify({"message" : "user with that email already exists"}), 400)

    @staticmethod
    def reset_password(user_id, password):
        """Reset user's password"""
        user = User.query.get(user_id)

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        if check_password_hash(user.password, password):
            return make_response(jsonify({"message" : "No changes detected"}), 400)

        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        return make_response(jsonify({
            "message" : "your password has been successfully reset",
            str(user.id) : {"username" : user.username,
                            "email" : user.email,
                            "admin" : user.admin}}), 200)


    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        user = User.query.get(user_id)

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)

    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        user = User.query.get(user_id)

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        records = Order.query.filter_by(user_id=user.id).all()
        orders = []
        for record in records:
            orders.append(str(record))

        info = {"user_id" : user.id, "email" : user.email,
                "username" : user.username, "admin" : user.admin,
                "orders" : orders}

        return make_response(jsonify({user.id : info}), 200)


class Meal(db.Model):
    """Contains meal columns and methods to add, update and delete a meal"""


    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    in_menu = db.Column(db.Boolean)


    def __repr__(self):
        return '<meal {}>'.format(self.name)

    @classmethod
    def create_meal(cls, name, price, in_menu=False):
        """Creates a new meal and ensures that the name is unique"""
        by_name = cls.query.filter_by(name=name).first()

        if by_name is None:
            new_meal = cls(name=name, price=price, in_menu=in_menu)
            db.session.add(new_meal)
            db.session.commit()
            return make_response(jsonify({
                "message" : "meal has been successfully created",
                str(new_meal.id) : {"name" : new_meal.name,
                                    "in_menu" : new_meal.in_menu,
                                    "price" : new_meal.price}}), 201)

        return make_response(jsonify({"message" : "meal with that name already exists"}), 400)

    @staticmethod
    def update_meal(meal_id, name, price, in_menu):
        """Updates meal information"""
        meal = Meal.query.get(meal_id)
        by_name = Meal.query.filter_by(name=name).first()

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if meal.name == name and meal.price == price and meal.in_menu == in_menu:
            return make_response(jsonify({"message" : "No changes detected"}), 400)

        if by_name is None or meal.id == by_name.id:
            meal.name = name
            meal.price = price
            meal.in_menu = in_menu
            db.session.commit()
            return make_response(jsonify({
                "message" : "meal has been successfully updated",
                str(meal.id) : {"name" : meal.name,
                                "in_menu" : meal.in_menu,
                                "price" : meal.price}}), 200)

        return make_response(jsonify({"message" : "meal with that name already exists"}), 400)

    @staticmethod
    def delete_meal(meal_id):
        """Deletes a meal"""
        meal = Meal.query.get(meal_id)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        db.session.delete(meal)
        db.session.commit()
        return make_response(jsonify({"message" : "meal has been successfully deleted"}), 200)

    @staticmethod
    def get_meal(meal_id):
        """Gets a particular meal"""
        meal = Meal.query.get(meal_id)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        info = {"meal_id" : meal.id, "name" : meal.name, "price" : meal.price, "in_menu" : meal.in_menu}
        return make_response(jsonify({meal.id : info}), 200)

    @staticmethod
    def add_to_menu(meal_id):
        """Adds a particular meal to the menu"""
        meal = Meal.query.get(meal_id)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if meal.in_menu:
            return make_response(jsonify({"message" : "meal already in the menu"}), 400)

        meal.in_menu = True
        db.session.commit()
        return make_response(jsonify({
            "message" : "meal has been successfully added to the menu",
            str(meal.id) : {"name" : meal.name,
                            "in_menu" : meal.in_menu,
                            "price" : meal.price}}), 200)

    @staticmethod
    def remove_from_menu(meal_id):
        """Removes a particular meal from the menu"""
        meal = Meal.query.get(meal_id)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if not meal.in_menu:
            return make_response(jsonify({"message" : "meal already not in the menu"}), 400)

        meal.in_menu = False
        db.session.commit()
        return make_response(jsonify({
            "message" : "meal has been successfully removed from the menu",
            str(meal.id) : {"name" : meal.name,
                            "in_menu" : meal.in_menu,
                            "price" : meal.price}}), 200)

    @staticmethod
    def get_menu(meal_id):
        """Gets a particular meal on the menu"""
        meal = Meal.query.get(meal_id)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if not meal.in_menu:
            return make_response(jsonify({
                "message" : "kindly ensure that this meal is in the menu"}), 400)

        info = {"meal_id" : meal.id, "name" : meal.name, "price" : meal.price, "in_menu" : meal.in_menu}
        return make_response(jsonify({meal.id : info}), 200)


class Order(db.Model):
    """Contains order columns and methods to add, update and delete an order"""


    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, nullable=False)
    meal_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_email = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')) # tablename

    def __repr__(self):
        return '<order {}: {}>'.format(self.id, self.meal_name)

    @classmethod
    def create_order(cls, meal_id, user_id):
        """Create a new order"""
        meal = Meal.query.get(meal_id)
        user = User.query.get(user_id)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        if not meal.in_menu:
            return make_response(jsonify({
                "message" : "kindly ensure that this meal is in the menu"}), 400)

        new_order = cls(meal_id=meal.id, meal_name=meal.name,
                        price=meal.price, user_id=user.id, user_email=user.email)
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify({
            "message" : "your order has been successfully created",
            str(new_order.id) : {"order_id" : new_order.id,
                                 "meal_id" : new_order.meal_id,
                                 "meal_name" : new_order.meal_name,
                                 "price" : new_order.price,
                                 "user_id" : new_order.user_id,
                                 "user_email" : new_order.user_email,
                                 "created_at" : new_order.created_at}}), 201)

    @staticmethod
    def update_order(order_id, meal_id):
        """Updates order information"""
        order = Order.query.get(order_id)
        meal = Meal.query.get(meal_id)

        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if not meal.in_menu:
            return make_response(jsonify({
                "message" : "kindly ensure that this meal is in the menu"}), 400)

        if order.meal_id == meal.id:
            return make_response(jsonify({"message" : "You had ordered this meal initially"}), 400)

        order.meal_id = meal.id
        order.meal_name = meal.name
        order.price = meal.price
        db.session.commit()
        return make_response(jsonify({
            "message" : "your order has been successfully updated",
            str(order.id) : {"order_id" : order.id,
                             "meal_id" : order.meal_id,
                             "meal_name" : order.meal_name,
                             "price" : order.price}}), 200)

    @staticmethod
    def delete_order(order_id):
        """Delete an order"""
        order = Order.query.get(order_id)

        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)

        db.session.delete(order)
        db.session.commit()
        return make_response(jsonify({"message" : "your order has been successfully deleted"}), 200)

    @staticmethod
    def get_order(order_id):
        """Get a particular order"""
        order = Order.query.get(order_id)

        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)

        info = {"order_id" : order.id,
                "meal_id" : order.meal_id,
                "meal_name" : order.meal_name,
                "price" : order.price,
                "user_id" : order.user_id,
                "user_email" : order.user_email,
                "created_at" : order.created_at}
        return make_response(jsonify({order.id : info}), 200)
