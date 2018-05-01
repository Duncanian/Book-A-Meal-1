"""Handles database migrations"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from models import db
from app import app


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

# $ python manage.py db init
# $ python manage.py db migrate
# $ python manage.py db upgrade
# $ python manage.py db --help
