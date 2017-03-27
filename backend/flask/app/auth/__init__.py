from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.auth import urls
from app.auth import models