"""Creates app instance, registers Blueprints and runs the Flask application
"""
from flask import Flask

from resources.meals import meals_api
from resources.users import users_api
from models import db


def create_app(configuration):
    """Create flask app"""
    app = Flask(__name__)
    app.config.from_object(configuration)
    app.url_map.strict_slashes = False

    app.register_blueprint(meals_api, url_prefix='/api/v3')
    app.register_blueprint(users_api, url_prefix='/api/v3')
    db.init_app(app)

    return app

app = create_app('config.ProductionConfig')


@app.route('/')
def hello_world():
    """test that flask app is running"""
    return 'Welcome to Book-A-Meal API'


if __name__ == '__main__':
    app.run() # run locally
