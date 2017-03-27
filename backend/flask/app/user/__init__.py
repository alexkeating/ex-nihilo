from flask import Blueprint

user = Blueprint('user', __name__)

import app.user.models
import app.user.views
import app.user.urls