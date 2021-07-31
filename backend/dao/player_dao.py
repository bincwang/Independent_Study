#This part is to operate database
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from db import engine

Base = declarative_base()
#Construct a base class for declarative class definitions.

class Player(Base):
    #Set up what I need for the database
    __tablename__ = 'players'
    username = Column(String(32), primary_key=True, nullable=False)
    password = Column(String(32), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    token = Column(String(32), nullable=True, unique=True)

    def __repr__(self):
        return "<Player(username='%s', password='%s', score='%s', token='%s')>" % (
            self.username, self.password, self.score, self.token)


Base.metadata.create_all(engine)
#Initialize databse (If I delete db file, it will create a db file for me)