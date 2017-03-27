from flask_restful import Api
restful_api = Api()

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from celery import Celery
celery = Celery()
