"""Contains various settings for each process of development
"""
from os import getenv


class Config(object):
    """Base class with all the constant config variables"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = getenv('SECRET_KEY')


class TestingConfig(Config):
    """Contains additional config variables required during testing"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('TESTING_DATABASE_URI')
    

class DevelopmentConfig(Config):
    """Contains additional config variables required during development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('DEVELOPMENT_DATABASE_URI')

class ProductionConfig(Config):
    """Contains config variables for use during production"""
    SQLALCHEMY_DATABASE_URI = getenv('PRODUCTION_DATABASE_URI')
