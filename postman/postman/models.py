
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
	)

Engine = None
Session = None
Base = declarative_base()

from sqlalchemy import (
		Column,
		Integer,
		Text,
		Date,
		Float,
		schema
	)



class Postman(Base):
	__tablename__ = 'Postman'
	id = Column(Integer, primary_key=True)
	idExternal = Column(Integer, unique=True)
	server = Column(Text)
	address = Column(Text)
	date = Column(Date)
	status = Column(Text)

	def __init__(self):
		pass

Postman_Attrs = [
	'idExternal',
	'server',
	'address',
	'status',
	'date'
]

