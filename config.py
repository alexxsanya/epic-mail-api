from os import environ

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('DATABASE_URL')
    JWT_SECRET_KEY = environ.get('SECRET_KEY') 

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config): 
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = environ.get("DATABASE_URL_TEST")

app_config = {
    "development" : DevelopmentConfig,
    "testing" : TestingConfig,
    "production" : ProductionConfig,
    "staging": StagingConfig
}