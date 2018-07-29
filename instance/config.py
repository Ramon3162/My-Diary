import os

class Config(object):
    """Parent configuration class"""

    DEBUG = False
    SECRET = os.getenv('SECRET')
    host = os.getenv('DB_HOST')
    db = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    APP_SETTINGS = 'development'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE = os.getenv('TEST_NAME')
    APP_SETTINGS = 'testing'

class StagingConfig(Config):
    """Staging configuration"""
    DEBUG = True
    APP_SETTINGS = 'staging'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    APP_SETTINGS = 'production'

app_config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'staging' : StagingConfig,
    'production' : ProductionConfig,
}
