"""Handles data storage for Users, Meals and Orders
"""
import json

all_users = {}
user_count = 1

all_meals = {}
meal_count = 1

all_menu = {}
menu_count = 1

class User(object):
    """Contains methods to add, update and delete a user"""


    @staticmethod
    def create_user(username, email, password, admin=False, **kwargs):
        """Creates a new user and appends his information to the all_users dictionary"""
        global all_users
        global user_count
        all_users[user_count] = {"id": user_count, "username" : username,
                         "email" : email, "password" : password, "admin" : admin}
        new_user = all_users[user_count]
        user_count += 1
        return new_user

    @staticmethod
    def update_user(user_id, username, email, password, admin=False, **kwargs):
        """Updates user information"""
        if user_id in all_users.keys():
            all_users[user_id] = {"id" : user_id, "username" : username, "email" : email,
                                  "password" : password, "admin" : admin}
            return all_users[user_id]
        return {"message" : "User does not exist"}

    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        try:
            del all_users[user_id]
            return {"message" : "User successfully deleted"}
        except KeyError:
            return {"message" : "User does not exist"}


class Meal(object):
    """Contains methods to add, update and delete a meal"""
    

    @staticmethod
    def create_meal(name, price, **kwargs):
        """Creates a new meal and appends this information to the all_meals dictionary"""
        global all_meals
        global meal_count
        all_meals[meal_count] = {"id": meal_count, "name" : name, "price": price}
        new_meal = all_meals[meal_count]
        meal_count += 1
        return new_meal

    @staticmethod
    def update_meal(meal_id, name, price, **kwargs):
        """Updates meal information"""
        if meal_id in all_meals.keys():
            all_meals[meal_id] = {"id": meal_id, "name" : name, "price" : price}
            return all_meals[meal_id]
        return {"message" : "Meal does not exist"}

    @staticmethod
    def delete_meal(meal_id):
        """Deletes a meal"""
        try:
            del all_meals[meal_id]
            return {"message" : "Meal successfully deleted"}
        except KeyError:
            return {"message" : "Meal does not exist"}


class Menu(object):
    """Contains methods to add, update and delete a meal from the menu"""


    @staticmethod
    def create_meal(name, price, **kwargs):
        """Creates a new meal and appends this information to the all_menu dictionary"""
        global all_menu
        global menu_count
        all_menu[menu_count] = {"id": menu_count, "name" : name, "price": price}
        new_menu_item = all_menu[menu_count]
        menu_count += 1
        return new_menu_item

    @staticmethod
    def update_meal(meal_id, name, price, **kwargs):
        """Updates meal information in menu"""
        if meal_id in all_menu.keys():
            all_menu[meal_id] = {"id": meal_id, "name" : name, "price" : price}
            return all_menu[meal_id]
        return {"message" : "Meal does not exist"}

    @staticmethod
    def delete_meal(meal_id):
        """Deletes a meal from the menu"""
        try:
            del all_menu[meal_id]
            return {"message" : "Meal successfully deleted"}
        except KeyError:
            return {"message" : "Meal does not exist"}