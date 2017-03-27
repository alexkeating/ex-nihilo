import os
from flask import Flask, render_template

from app.database import db
from app.extensions import (bcrypt, restful_api, celery)
from app.api import api
from app.auth import auth
from app.user import user


config = os.getenv('APP_SETTINGS')


def create_app(config=config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    bcrypt.init_app(app)
    restful_api.init_app(app)
    celery.config_from_object(app.config)
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api)
    app.register_blueprint(user)
    app.register_blueprint(auth)


