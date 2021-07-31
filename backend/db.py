#This part is for configuring database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
#https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html
path = "game.db"
engine = create_engine("sqlite:///{}".format(path))
#The create_engine() function produces an Engine object based on a URL
#Just an assistance to connect with database
#We could build a new session with database with this engine

def connect() -> Session:
    session_class = sessionmaker(bind=engine)
    return session_class()
#https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference