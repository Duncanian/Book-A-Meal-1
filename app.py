"""Creates app instance, registers Blueprints and runs the Flask application
"""
import os

from flask import Flask

from resources.meals import meals_api
from resources.users import users_api


def create_app():
    """Create flask app"""
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.url_map.strict_slashes = False

    app.register_blueprint(meals_api, url_prefix='/api/v1')
    app.register_blueprint(users_api, url_prefix='/api/v1')

    return app

app = create_app()


@app.route('/')
def hello_world():
    "test that flask app is running"
    return 'Welcome to Book-A-Meal API'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('', port=port)
