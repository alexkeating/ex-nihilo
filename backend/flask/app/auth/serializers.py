from flask import jsonify

from app.api.serializers import GenericSerializer
from app.auth.models import BlacklistToken
from app.user.models import User


class AuthSerializer(GenericSerializer):
    TABLE_MODEL = User

    def create(self, json):
        user = self.TABLE_MODEL(
            email=json.get('email'),
            password=json.get('password')
        )

        # insert the user
        user.create()
        auth_token = user.encode_auth_token(user.id)
        response = {
            'status': 'success',
            'message': 'Successfully registered.',
            'auth_token': auth_token.decode()
        }

        return jsonify(response)


class BlacklistTokenSerializer(GenericSerializer):
    TABLE_MODEL = BlacklistToken

    @staticmethod
    def create(headers):
        auth_header = headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]
        blacklist_token = BlacklistToken(token=auth_token)
        blacklist_token.create()
        response = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return jsonify(response)


