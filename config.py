from os import environ


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URL = environ.get('DATABASE_URL')
    JWT_SECRET_KEY = environ.get('SECRET_KEY', 'secrete')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = environ.get("DEV_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = environ.get("TEST_DATABASE_URL")


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "staging": StagingConfig
}