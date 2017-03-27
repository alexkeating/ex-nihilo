import os

from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import import_string


db = SQLAlchemy()
settings = os.getenv('APP_SETTINGS')

config = import_string(settings)


def connection():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    conn = engine.connect()
    return conn


def execute_statement(func):
    conn = connection()

    def wrapper(*args, **kwargs):
        statement = func(*args, **kwargs)
        conn.execute(statement)
    return wrapper


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, basestring) and id.isdigit(),
                isinstance(id, (int, float))),):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get_or_create(cls, model_id=None, **kwargs):
        try:
            created = False
            instance = cls.query.filter(id=model_id).one()
        except NoResultFound:
            created = True
            instance = cls.create(**kwargs)
        return instance, created

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class TimeStampMixin(object):
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(timezone=True),
                           onupdate=db.func.current_timestamp())
