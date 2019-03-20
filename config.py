from os import environ

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False

class StagingConfig(Config):
    ENV = "staging"
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    ENV = "testing"
    DEBUG = True