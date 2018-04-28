"""Creates app instance, registers Blueprints and runs the Flask application
"""
import os

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

from resources.meals import meals_api
from resources.users import users_api

def create_app():
    """Create flask app"""
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.url_map.strict_slashes = False

    app.register_blueprint(meals_api, url_prefix='/api/v1')
    app.register_blueprint(users_api, url_prefix='/api/v1')

    # set up limiter to prevent Dos attacks
    DEFAULT_RATE = "150/hour"
    limiter = Limiter(app, default_limits=[DEFAULT_RATE], key_func=get_ipaddr)
    limiter.limit(DEFAULT_RATE, per_method=True, methods=['POST', 'PUT', 'DELETE'])(users_api) 
    limiter.limit(DEFAULT_RATE, per_method=True, methods=['POST', 'PUT', 'DELETE'])(meals_api)

    return app

app = create_app()

@app.route('/')
def hello_world():
    "test that flask app is running"
    return 'Hello World'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('', port=port)
