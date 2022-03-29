import random
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Passworduser(Base):
    """ Password Manager user """

    __tablename__ = "password_user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    # trace_id = Column(String(100), nullable=False)
    trace_id = Column(Integer, nullable=False)

    def __init__(self, user_id, name, password, email, trace_id):
        """ Initializes a user of password manager """
        self.user_id = user_id
        self.name = name
        self.date_created = datetime.datetime.now()  # Sets the date/time record is created
        self.password = password
        self.email = email
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a password user """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['name'] = self.name
        dict['password'] = self.password
        dict['email'] = self.email
        dict['date_created'] = self.date_created.strftime(
                   "%Y-%m-%dT%H:%M:%SZ")
        dict['trace_id'] = self.trace_id

        return dict
