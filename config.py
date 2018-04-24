"""Contains various settings for each process of development
Created: April 2018
Author: Lenny
"""

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "!@#_)&^%$$epic8^%%$#@#%^&*(&^&"


class TestingConfig(Config):
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True

# class ProductionConfig(Config):