
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main.server import ConnectDB
from collections import namedtuple


engine  = ConnectDB()
# an Engine, which the Session will use for connection
# resources
some_engine = engine.cur
# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship

Base = declarative_base()

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    word = Column(String(50))
    translate = Column(String(50))
    deckid = Column(Integer)
    userid =  Column(Integer)
    
    def __init__(self,word, translate, deckid, userid):
    
        self.word = word 
        self.translate = translate 
        self.deckid = deckid 
        self.userid = userid 

session.add(Card('word1', 'translate1', '1', '1'))
session.commit()