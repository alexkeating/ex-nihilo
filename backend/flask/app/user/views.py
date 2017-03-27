from flask import request
from flask_restful import reqparse, abort, Api, Resource
from app.user.serializers import UserSerializer


class User(Resource):
    serializer = UserSerializer()
    json = None

    def dispatch_request(self, *args, **kwargs):
        self.json = request.get_json()
        resp = super().dispatch_request(*args, **kwargs)
        return resp

    def get(self):
        user = self.serializer.get(self.json)
        return user

    def delete(self):
        self.serializer.remove(self.json)
        return 204

    def put(self):
        self.serializer.create_or_modify(self.json)
        return 201

    def post(self):
        self.serializer.create(self.json)
        return 200
