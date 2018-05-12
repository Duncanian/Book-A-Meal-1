"""Handles database migrations and handles superuser creation"""
import re
import sys

from flask_script import Manager, prompt, prompt_pass
from flask_migrate import Migrate, MigrateCommand

from models import db, User
from app import app


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@manager.command
def createsuperuser():
    """Create a superuser, requires username, email and password."""

    username = prompt('superuser username')

    email = prompt('superuser email')
    confirm_email = prompt('confirm superuser email')

    if not EMAIL_REGEX.match(email):
        sys.exit('\n kindly provide a valid email address')

    if not email == confirm_email:
        sys.exit('\n kindly ensure that email and confirm email are identical')

    password = prompt_pass('superuser password')
    confirm_password = prompt_pass('confirm superuser password')

    if not password == confirm_password:
        sys.exit('\n kindly ensure that password and confirm password are identical')
    
    User.create_user(
        username=username,
        email=email,
        password=password,
        admin=True)


if __name__ == '__main__':
    manager.run()
    db.create_all()

# $ python manage.py db init
# $ python manage.py db migrate
# $ python manage.py db upgrade
# $ python manage.py db --help
