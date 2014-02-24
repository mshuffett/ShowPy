from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import datetime


Base = declarative_base()


class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})): pass


class Db(Singleton):
    '''
    The DB Class should only exits once, thats why it has the @Singleton decorator.
    To Create an instance you have to use the instance method:
        db = Db.instance()
    '''
    engine = None
    session = None

    def __init__(self):
        print 'this should only be called once'
        self.engine = create_engine('sqlite:///showpy.db', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        ## Create all Tables
        Base.metadata.create_all(self.engine)


class ModelMixin(object):
    '''
    This is a baseclass with delivers all basic database operations
    '''

    @declared_attr
    def __tablename__(cls):
        '''Get table name from class name'''
        return cls.__name__.lower()

    def save(self):
        db = Db.instance()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def save_multiple(objects):
        db = Db.instance()
        db.session.add_all(objects)
        db.session.commit()

    def update(self):
        db = Db.instance()
        db.session.commit()

    def delete(self):
        db = Db.instance()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete(cls):
        db = Db.instance()
        db.session.query(cls).delete()
        db.session.commit()

    @classmethod
    def query(cls):
        db = Db.instance()
        return db.session.query(cls)

    @classmethod
    def all(cls):
        return cls.query().all()


class Show(ModelMixin, Base):
    title = Column(String, primary_key=True)

    def __repr__(self):
        return "<Show(title='%s')>" % self.title


class Setting(ModelMixin, Base):
    key = Column(String, primary_key=True)
    value = Column(String, primary_key=True)

    def __repr__(self):
        return "<Setting(key='%s', value='%s')>" % (self.key, self.value)