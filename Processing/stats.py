from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Stats(Base):
    """ Processing Statistics """

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_of_name = Column(Integer, nullable=False)
    num_of_password = Column(Integer, nullable=False)
    max_length_password = Column(Integer, nullable=False)
    trace_id = Column(Integer, nullable=True)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, num_of_name, num_of_password, max_length_password, trace_id, last_updated):
        """ Initializes a processing statistics objet """
        self.num_of_name = num_of_name
        self.num_of_password = num_of_password
        self.max_length_password = max_length_password
        self.trace_id = trace_id
        self.last_updated = last_updated

    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['num_of_name'] = self.num_of_name
        dict['num_of_password'] = self.num_of_password
        dict['max_length_password'] = self.max_length_password
        dict['trace_id'] = self.trace_id
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")

        return dict
