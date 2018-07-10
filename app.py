"""Creates app instance, registers Blueprints and runs the Flask application
"""
from flask import Flask, render_template

from resources.users import users_api
from resources.account import account_api
from resources.meals import meals_api
from resources.menu import menu_api
from resources.orders import orders_api
from models import db


def create_app(configuration):
    """Create flask app"""
    app = Flask(__name__)
    app.config.from_object(configuration)
    app.url_map.strict_slashes = False

    app.register_blueprint(users_api, url_prefix='/api/v3')
    app.register_blueprint(account_api, url_prefix='/api/v3')
    app.register_blueprint(meals_api, url_prefix='/api/v3')
    app.register_blueprint(menu_api, url_prefix='/api/v3')
    app.register_blueprint(orders_api, url_prefix='/api/v3')
    db.init_app(app)

    return app

app = create_app('config.DevelopmentConfig')


@app.route('/')
def hello_world():
    """test that flask app is running"""
    return 'Welcome to Book-A-Meal API'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8000) # run locally
