
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
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()

user = Table('user', metadata,
             Column('id', Integer, primary_key=True),
             Column('login', String(50)),
             Column('password', String(12))
             )

card = Table('cards', metadata,
                Column('id', Integer, primary_key=True),
                Column('word', String(50)),
                Column('translate', String(50)),
                Column('deckid', Integer),
                Column('userid', Integer, ForeignKey('user.id')),
                )

from main.server import Card
class User(object):
    pass

print(dir(User))

mapper(
    User, user,
    properties={
        'cards': relationship(Card, backref='user',
                                  order_by=card.c.id)
    })

print(dir(User))

mapper(Card, card)
session.add(Card('word', 'translate'))
session.commit()