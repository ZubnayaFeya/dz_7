from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ForeignKey
from system_d.config import *


Base = declarative_base()

path_db = '{}servers_d/db/'.format(path_project)

engine = create_engine('sqlite:///{}server.db'.format(path_db), echo=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User({}, {}, {})>".format(self.name, self.fullname, self.password)

    def auth_user(self):
        pass

    def check_auth(self, name, password):
        pass

    def del_user(self, name):
        pass

    def update_user(self):
        pass


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer)
    in_time = Column(String)
    ip_address = Column(String)

    def __init__(self, id_user, in_time, ip_address):
        self.id_user = id_user
        self.in_time = in_time
        self.ip_address = ip_address

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.id_user, self.in_time, self.ip_address)


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('User.id'))
    id_contacts = Column(Integer, ForeignKey('User.id'))

    def __init__(self, id_user, id_contacts):
        self.id_user = id_user
        self.id_contacts = id_contacts

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.id_user, self.id_contacts)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()  # можно через менеджер контекста



