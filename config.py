"""Contains various settings for each process of development
"""

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "!@#_)&^%$$epic8^%%$#@#%^&*(&^&"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True
