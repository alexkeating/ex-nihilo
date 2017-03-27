from flask import request, make_response, jsonify

from app.user.models import User


def is_authenticated(func):
    def wrapper(*args, **kwargs):
        auth_token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            user = User.query.filter_by(id=resp).first()
            if user:
                view = func(*args, **kwargs)
                return view
            else:
                response = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response)), 401
    return wrapper

