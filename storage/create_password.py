import random
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Userpasswords(Base):
    """ User's passwords """

    __tablename__ = "user_password"

    id = Column(Integer, primary_key=True)
    password_id = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    password_hint = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    description = Column(String(250), nullable=False)
    # trace_id = Column(String(100), nullable=False)
    trace_id = Column(Integer, nullable=False)

    def __init__(self, password_id, password, password_hint, description, trace_id):
        """ Initializes a password """
        self.password_id = password_id
        self.password = password
        self.password_hint = password_hint
        self.date_created = datetime.datetime.now()  # Sets the date/time record is created
        self.description = description
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of passwords in the accounts """
        dict = {}
        dict['id'] = self.id
        dict['password_id'] = self.password_id
        dict['password'] = self.password
        dict['password_hint'] = self.password_hint
        dict['description'] = self.description
        dict['date_created'] = self.date_created.strftime(
                   "%Y-%m-%dT%H:%M:%SZ")
        dict['trace_id'] = self.trace_id

        return dict
