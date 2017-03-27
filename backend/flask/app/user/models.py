import datetime
import jwt
import os
from werkzeug.utils import import_string

from app.extensions import cache, bcrypt
from app.database import db, CRUDMixin, TimeStampMixin
from app.auth.models import BlacklistToken


settings = os.getenv('APP_SETTINGS')
config = import_string(settings)


class User(CRUDMixin, TimeStampMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.Binary(60), nullable=False)

    def __init__(self, email, password, first_name=None, last_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<User %s>' % self.email

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password, config.BCRYPT_LOG_ROUNDS)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
