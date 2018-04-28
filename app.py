"""Creates app instance, registers Blueprints and runs the Flask application
"""
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
    return 'Hello World'


if __name__ == '__main__':
    app.run(port=5000)
