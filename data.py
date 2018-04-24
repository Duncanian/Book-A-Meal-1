import json
all_users = {}
user_id = 1

all_meals = {}
meal_id = 1

class User(object):
    """Contains methods to add, update and delete a user"""
    def __init__(self, id, username, email, password, admin=False):
        """Initializes important variables required"""
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin


    @classmethod
    def create_user(cls, username, email, password, admin=False, **kwargs):
        """Creates a new user and appends his information to the all_users dictionary"""
        global all_users
        global user_id
        user = cls(id=user_id, username=username, email=email, password=password, admin=admin)
        all_users[user.id] = {"id": user.id, "username" : user.username,
                              "email" : user.email, "password" : user.password, "admin" : user.admin}
        user_id += 1
        return all_users[user.id]

    @staticmethod
    def update_user(id, username, email, password, admin=False, **kwargs):
        """Updates user information"""
        if id in all_users.keys():
            all_users[id] = {"id" : id, "username" : username, "email" : email, "password" : password, "admin" : admin}
        return json.dumps({"message" : "User does not exist"})

    @staticmethod
    def delete_user(id):
        """Deletes a user"""
        try:
            del all_users[id]
            return json.dumps({"message" : "User successfully deleted not exist"})
        except KeyError:
            json.dumps({"message" : "User does not exist"})
        


    @staticmethod
    def get_credentials(id, credential):
        if credential == "username":
            return all_users.get(id)["username"]
        if credential == "email":
            return all_users.get(id)["email"]
        if credential == "password":
            return all_users.get(id)["password"]
        if credential == "admin":
            return all_users.get(id)["admin"]


class Meal(object):
    """Contains methods to add, update and delete a user"""
    def __init__(self, id, item, price):
        """Initializes important variables required"""
        self.id = id
        self.item = item
        self.price = price

    @classmethod
    def create_meal(cls, id, item, price, **kwargs):
        """Creates a new meal and appends this information to the all_meals dictionary"""
        global all_meals
        global meal_id
        meal = cls(id=meal_id, item=item, price=price)
        all_meals[meal.id] = {"id": meal.id, "item" : meal.item,
                              "price" : meal.price}
        meal_id += 1

    @staticmethod
    def update_meal(id, item, price, **kwargs):
        """Updates meal information"""
        if id in all_meals.keys():
            all_meals[id] = {"id": id, "item" : item, "price" : price}
        return json.dumps({"message" : "Meal does not exist"})

    @staticmethod
    def delete_meal(id):
        """Deletes a meal"""
        try:
            del all_meals[id]
            return json.dumps({"message" : "Meal successfully deleted not exist"})
        except KeyError:
            json.dumps({"message" : "Meal does not exist"})
