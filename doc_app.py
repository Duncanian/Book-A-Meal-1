"""Contain interactive documentation to help one get started using the API
"""
import os

from flask import render_template
from flasgger import Swagger

from app import create_app


app = create_app('config.ProductionConfig')
swagger = Swagger(app)


# Users
@app.route('/api/v3/auth/signup/', methods=["POST"])
def signup():
    """ endpoint for registering users.
    ---
    parameters:
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
    """

@app.route('/api/v3/auth/login', methods=["POST"])
def login():
    """ endpoint for logging in users.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    """

@app.route('/api/v3/auth/reset/', methods=["POST"])
def reset():
    """ endpoint for resetting one's password.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: current_password
        in: formData
        type: string
        required: true
      - name: new_password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
    """

# to be be secured
@app.route('/api/v3/users', methods=["POST"])
def users_create():
    """ endpoint for creating users.
    ---
    parameters:
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: admin
        in: formData
        type: boolean
        required: false
        default: false
    """

@app.route("/api/v3/users", methods=["GET"])
def get_all_users():
    """endpoint for  getting all users.
     ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v3/users/<int:user_id>", methods=["GET"])
def get_one_user():
    """endpoint for  getting a particular user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: user_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v3/users/<int:user_id>', methods=["PUT"])
def update_user():
    """ endpoint for updating an existing user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v3/users/<int:user_id>', methods=["DELETE"])
def delete_user():
    """ endpoint for deleting an existing user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: user_id
        in: path
        type: integer
        required: true
    """


# Meals
@app.route('/api/v3/meals', methods=["POST"])
def create_meal():
    """ endpoint for creating a meal item.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: name
        required: true
        in: formData
        type: string
      - name: price
        in: formData
        type: integer
        required: true
      - name: in_menu
        in: formData
        type: boolean
        required: true
        default: false
    """

@app.route("/api/v3/meals", methods=["GET"])
def get_all_meals():
    """endpoint for getting all meals.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v3/meals/<int:meal_id>", methods=["GET"])
def get_one_meal():
    """endpoint for  getting a particular meal.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v3/meals/<int:meal_id>', methods=["PUT"])
def update_meal():
    """ endpoint for updating an existing meal.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: path
        type: integer
        required: true
      - name: name
        in: formData
        type: string
        required: true
      - name: price
        in: formData
        type: integer
        required: true
      - name: in_menu
        in: formData
        type: boolean
        required: true
        default: false
    """

@app.route('/api/v3/meals/<int:meal_id>', methods=["DELETE"])
def delete_meal():
    """ endpoint for deleting an existing meal.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: path
        type: integer
        required: true
    """


# Menu
@app.route('/api/v3/menu', methods=["POST"])
def create_menu():
    """ endpoint for creating a menu option.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: formData
        type: integer
        required: true
    """

@app.route("/api/v3/menu", methods=["GET"])
def get_all_menu():
    """endpoint for  getting all menu options.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v3/menu/<int:meal_id>", methods=["GET"])
def get_one_menu_option():
    """endpoint for getting a particular menu option.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v3/menu/<int:meal_id>', methods=["DELETE"])
def delete_menu():
    """ endpoint for removing a meal form the menu.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: path
        type: integer
        required: true
    """


# Orders
@app.route('/api/v3/orders', methods=["POST"])
def create_order():
    """ endpoint for creating an order item.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: meal_id
        in: formData
        type: integer
        required: true
    """

@app.route("/api/v3/orders", methods=["GET"])
def get_all_orders():
    """endpoint for  getting all orders.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v3/orders/<int:order_id>", methods=["GET"])
def get_one_order():
    """endpoint for  getting a particular order.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: order_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v3/orders/<int:order_id>', methods=["PUT"])
def update_order():
    """ endpoint for updating an existing order.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: order_id
        in: path
        type: integer
        required: true
      - name: meal_id
        in: formData
        type: integer
        required: true
    """

@app.route('/api/v3/orders/<int:order_id>', methods=["DELETE"])
def delete_order():
    """ endpoint for deleting an existing order.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: order_id
        in: path
        type: integer
        required: true
    """

@app.route('/')
def hello_world():
    "test that flask app is running"
    return "To view the docs visit: https://book-a-meal-api.herokuapp.com/apidocs"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('', port=port)
