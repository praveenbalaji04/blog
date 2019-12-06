from flask import Flask


def create_app(config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    return flask_app
