from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import datetime

_Base = declarative_base()
_engine = create_engine('sqlite:///showpy.db', echo=True)
## Create all Tables
_Base.metadata.create_all(_engine)
_Session = sessionmaker(bind=_engine)
session = _Session()


class ModelMixin(object):
    '''
    This is a baseclass with delivers all basic database operations
    '''

    @declared_attr
    def __tablename__(cls):
        '''Get table name from class name'''
        return cls.__name__.lower()

    def save(self):
        session.add(self)
        session.commit()

    @staticmethod
    def save_multiple(objects):
        session.add_all(objects)
        session.commit()

    def update(self):
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @classmethod
    def delete(cls):
        session.query(cls).delete()
        session.commit()

    @classmethod
    def query(cls):
        return session.query(cls)

    @classmethod
    def all(cls):
        return cls.query().all()


class Show(ModelMixin, _Base):
    title = Column(String, primary_key=True)

    def __repr__(self):
        return "<Show(title='%s')>" % self.title


class Setting(ModelMixin, _Base):
    key = Column(String, primary_key=True)
    value = Column(String, primary_key=True)

    def __repr__(self):
        return "<Setting(key='%s', value='%s')>" % (self.key, self.value)