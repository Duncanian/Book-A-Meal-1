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


    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean)

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
                "password" : new_user.password,
                "admin" : new_user.admin}}), 201)


        return make_response(jsonify({"message" : "user with that email already exists"}), 400)


    @staticmethod
    def update_user(user_id, username, email, password, admin=False):
        """Updates user information"""
        user = User.query.get(user_id)
        by_email = User.query.filter_by(email=email).first()
        
        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        if by_email is None:
            user.username = username
            user.email = email
            user.password = generate_password_hash(password, method='sha256')
            user.admin = admin
            db.session.commit()
            return make_response(jsonify({
                "message" : "user has been successfully updated",
                str(user.id) : {"username" : user.username,
                "email" : user.email,
                "password" : user.password,
                "admin" : user.admin}}), 200)

        return make_response(jsonify({"message" : "user with that email already exists"}), 400)


    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({"message" : "user does not exists"}), 404)
        
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)


    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({"message" : "user does not exists"}), 404)
        
        info = {"user_id" : user.id, "email" : user.email,
                "username" : user.username, "password" : user.password,
                "admin" : user.admin}

        return make_response(jsonify({user.id : info}), 200)


class Meal(db.Model):
    """Contains meal columns and methods to add, update and delete a meal item"""


    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    meal_item = db.Column(db.String(250), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<meal {}>'.format(self.meal_item)


    @classmethod
    def create_meal(cls, meal_item, price):
        """Creates a new meal item and ensures that the name is unique"""
        by_name = cls.query.filter_by(meal_item=meal_item).first()

        if by_name is None:
            new_meal = cls(meal_item=meal_item, price=price)
            db.session.add(new_meal)
            db.session.commit()
            return make_response(jsonify({
                "message" : "meal item has been successfully created",
                str(new_meal.id) : {"meal_item" : new_meal.meal_item,
                "price" : new_meal.price}}), 201)

        return make_response(jsonify({"message" : "meal item with that name already exists"}), 400)

    @staticmethod
    def update_meal(meal_id, meal_item, price):
        """Updates meal item information"""
        meal = Meal.query.get(meal_id)
        by_name = Meal.query.filter_by(meal_item=meal_item).first()

        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)

        if by_name is None:
            meal.meal_item = meal_item
            meal.price = price
            db.session.commit()
            return make_response(jsonify({
                "message" : "meal has been successfully updated",
                str(meal.id) : {"meal_item" : meal.meal_item,
                "price" : meal.price}}), 200)

        return make_response(jsonify({"message" : "meal item with that name already exists"}), 400)

    @staticmethod
    def delete_meal(meal_id):
        """Deletes a meal"""
        meal = Meal.query.get(meal_id)
        
        if not meal:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)
        
        db.session.delete(meal)
        db.session.commit()
        return make_response(jsonify({"message" : "meal has been successfully deleted"}), 200)
    
    @staticmethod
    def get_meal(meal_id):
        """Gets a particular meal item"""
        meal = Meal.query.get(meal_id)
        
        if meal is None:
            return make_response(jsonify({"message" : "meal does not exists"}), 404)
        
        info = {"id" : meal.id, "meal_item" : meal.meal_item, "price" : meal.price}
        return make_response(jsonify({meal.id : info}), 200)


class Menu(db.Model):
    """Contains menu columns and methods to add, update and delete a menu option"""
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    menu_option = db.Column(db.String(250), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<menu option {}>'.format(self.menu_option)


    @classmethod
    def create_menu(cls, menu_option, price):
        """Creates a new menu option and ensures that the name is unique"""
        by_name = cls.query.filter_by(menu_option=menu_option).first()
        in_meals = Meal.query.filter_by(meal_item=menu_option).first()

        if by_name is None:
            if in_meals is None:
                return make_response(jsonify({
                    "message" : "kindly add the item to the meals tables before adding it in the menu"}), 400)

            new_menu = cls(menu_option=menu_option, price=price)
            db.session.add(new_menu)
            db.session.commit()
            return make_response(jsonify({
                "message" : "menu option has been successfully created",
                str(new_menu.id) : {"menu_option" : new_menu.menu_option,
                "price" : new_menu.price}}), 201)

        return make_response(jsonify({"message" : "menu option with that name already exists"}), 400)

    @staticmethod
    def update_menu(menu_id, menu_option, price):
        """Updates menu option information"""
        menu = Menu.query.get(menu_id)
        in_meals = Meal.query.filter_by(meal_item=menu_option).first()
        
        if menu is None:
            return make_response(jsonify({"message" : "menu option does not exists"}), 404)

        if in_meals is None:
                return make_response(jsonify({
                    "message" : "kindly add the item to the meals table before adding it in the menu"}), 400)
        menu.menu_option = menu_option
        menu.price = price
        db.session.commit()
        return make_response(jsonify({
            "message" : "menu option has been successfully updated",
            str(menu.id) : {"menu_option" : menu.menu_option,
            "price" : menu.price}}), 200)


    @staticmethod
    def delete_menu(menu_id):
        """Deletes a meal"""
        menu = Menu.query.get(menu_id)
        
        if menu is None:
            return make_response(jsonify({"message" : "menu option does not exists"}), 404)
        
        db.session.delete(menu)
        db.session.commit()
        return make_response(jsonify({"message" : "menu option has been successfully deleted"}), 200)
    
    @staticmethod
    def get_menu(menu_id):
        """Gets a particular menu option"""
        menu = Menu.query.get(menu_id)
        
        if menu is None:
            return make_response(jsonify({"message" : "menu option does not exists"}), 404)
        
        info = {"menu_id" : menu.id, "menu_option" : menu.menu_option, "price" : menu.price}
        return make_response(jsonify({menu.id : info}), 200)


class Order(db.Model):
    """Contains order columns and methods to add, update and delete an order item"""
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_item = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    client_email = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    

    def __repr__(self):
        return '<order {}>'.format(self.order_item)


    @classmethod
    def create_order(cls, order_item, price, client_id, client_email):
        """Creates a new order item"""
        in_menu = Menu.query.filter_by(menu_option=order_item).first()

        if in_menu is None:
                return make_response(jsonify({
                    "message" : "kindly ensure that your order item is in the menu"}), 400)
        
        new_order = cls(order_item=order_item, price=price, client_id=client_id, client_email=client_email)
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify({
            "message" : "order has been successfully created",
            str(new_order.id) : {"order_item" : new_order.order_item,
            "price" : new_order.price, "client_id" : new_order.client_id,
            "client_email" : new_order.client_email,
            "created_at" : new_order.created_at}}), 200) # match status code of time limit

    @staticmethod
    def update_order(order_id, order_item, price):
        """Updates order item information"""
        order = Order.query.get(order_id)
        in_menu = Menu.query.filter_by(menu_option=order_item).first()
        
        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)
    
        if in_menu is None:
                return make_response(jsonify({
                    "message" : "kindly ensure that your order item is in the menu"}), 400)
        order.order_item = order_item
        order.price = price
        db.session.commit()
        return make_response(jsonify({
            "message" : "order has been successfully updated",
            str(order.id) : {"order_item" : order.order_item,
            "price" : order.price}}), 200)

    @staticmethod
    def delete_order(order_id):
        """Deletes an order"""
        order = Order.query.get(order_id)
        
        if order is None:
            return make_response(jsonify({"message" : "order does not exists"}), 404)
        
        db.session.delete(order)
        db.session.commit()
        return make_response(jsonify({"message" : "order has been successfully deleted"}), 200)
    
    @staticmethod
    def get_order(order_id):
        """Gets a particular order item"""
        order = Order.query.get(order_id)
        
        if order is None:
            return make_response(jsonify({"message" : "order item does not exists"}), 404)
        
        info = {"order_id" : order.id, "order_item" : order.order_item, "price" : order.price,
                "client_id" : order.client_id, "client_email" : order.client_email,
                "created_at" : order.created_at}
        return make_response(jsonify({order.id : info}), 200)
