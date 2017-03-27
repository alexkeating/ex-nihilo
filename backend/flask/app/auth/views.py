import bcrypt

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView


from app.api.decorators import is_authenticated
from app.database import db
from app.user.models import User
from app.auth.models import BlacklistToken
from app.auth.serializers import AuthSerializer, BlacklistTokenSerializer


class RegisterAPI(MethodView):
    """
    This view is used when a user registers for the website.
    It checks to see if a user exists. New users
    """
    serializer = AuthSerializer()

    def post(self):
        json = request.get_json()
        email = json.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            response = self.serializer.create(json)
            return make_response(response, 201)
        else:
            response = self.serializer.resp_202()
            return make_response(response, 202)


class LoginAPI(MethodView):
    """
    For when a user logs in.
    """
    serializer = AuthSerializer()

    def post(self):
        json = request.get_json()
        email = json.get('email')
        password = json.get('password')

        user = User.query.filter_by(
            email=email
          ).first()
        valid_password = bcrypt.check_password_hash(user.password, password)
        if user and valid_password:
            response = self.serializer.create(json)
            return make_response(response, 200)
        else:
            response = self.serializer.resp_404()
            return make_response(response, 404)


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    decorators = [is_authenticated]
    serializer = BlacklistTokenSerializer()

    def post(self):
        headers = request.headers
        response = self.serializer.create(headers)
        return make_response(response, 200)


