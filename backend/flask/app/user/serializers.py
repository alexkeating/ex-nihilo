# It is just a reprentation of data for the view
from app.api.serializers import GenericSerializer
from app.user.models import User


class UserSerializer(GenericSerializer):
    TABLE_MODEL = User

    def get(self):
        pass

    @staticmethod
    def create(json):
        User.create(**json)
