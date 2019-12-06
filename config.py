import os


class Config:
    DEBUG = True
    PORT = 5000
    HOST = "0.0.0.0"
    MONGODB_NAME = "blog"
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG = False


app_config = DevelopmentConfig
if os.environ.get('FLASK_CONFIG') == 'production':
    app_config = ProductionConfig
