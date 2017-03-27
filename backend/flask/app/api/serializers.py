from abc import abstractmethod
from flask import jsonify
from sqlalchemy import insert, update, delete

from app.database import execute_statement
from app.exceptions import MissingIdException

# to save keys will be sent and they will be saved
# An update the frontend should only send things that have been changed
# A delete will delete the instance
# A get with get the necessary data representation for the page


class AbstractSerializer(object):

    @classmethod
    @abstractmethod
    def create(self, json):
        pass

    @classmethod
    @abstractmethod
    def modify(self, json):
        pass

    @classmethod
    @abstractmethod
    def remove(self, json):
        pass

    @classmethod
    @abstractmethod
    def create_or_update(self, json):
        pass

    @classmethod
    @abstractmethod
    def get(self, model_id):
        pass


class ErrorSerializerMixin(object):

    @staticmethod
    def resp_202():
        response = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return jsonify(response)


class GenericSerializer(AbstractSerializer, ErrorSerializerMixin):
    TABLE_MODEL = None

    def __init__(self):
        if not self.TABLE_MODEL:
            raise ValueError('Missing value for table model')

    @execute_statement
    def create(self, json):
        """

        :param json:
        :return:
        """
        statement = insert(self.TABLE_MODEL).values(**json)
        return statement

    @execute_statement
    def modify(self, json):
        """

        :param json:
        :return:
        """
        statement = update(self.TABLE_MODEL).values(**json)
        return statement

    @execute_statement
    def remove(self, model_id):
        model_id = self.TABLE_MODEL.id
        delete(self.TABLE_MODEL).where(model_id=model_id)

    @execute_statement
    def get(self, model_id):
        pass

    def create_or_update(self, json):
        """

        :param json:
        :return:
        """
        if 'id' not in json:
            raise MissingIdException('No id in the api payload')
        model_id = json.get('id')
        self.TABLE_MODEL.get_or_create(id=model_id)