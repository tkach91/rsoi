
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




class Catalogue(Base):
	__tablename__ = 'Catalogue'
	id = Column(Integer, primary_key=True)
	idCatalogue = Column(Integer, unique=True, nullable=False)
	name = Column(Text)
	description = Column(Text)
	price = Column(Float)

	def __init__(self):
		pass

Catalogue_Attrs = [
	'idCatalogue',
	'name',
	'description',
	'price'
]



class Orders(Base):
	__tablename__ = 'Orders'
	id = Column(Integer, primary_key=True)
	idUser = Column(Integer, schema.ForeignKey('Users.id'), nullable=False)
	address = Column(Text)
	date = Column(Date)
	warehouses = Column(Integer, default=0)
	status = Column(Text)

	def __init__(self):
		pass

Orders_Attrs = [
	'idUser',
	'address',
	'date',
	'warehouses',
	'status'
]



class Orders_Catalogue(Base):
	__tablename__ = 'Orders_Catalogue'
	id = Column(Integer, primary_key=True)
	idOrder = Column(Integer, schema.ForeignKey('Orders.id'), nullable=True)
	idCatalogue = Column(Integer, schema.ForeignKey('Catalogue.idCatalogue'), nullable=False)
	count = Column(Integer)

	def __init__(self):
		pass

Orders_Catalogue_Attrs = [
	'idOrder',
	'idCatalogue',
	'count'
]

class Users(Base):
	__tablename__ = 'Users'
	id = Column(Integer, primary_key=True)
	username = Column(Text)
	password = Column(Text)

	def __init__(self):
		pass

Users_Attrs = [
	'username',
	'password'
]

class Admins(Base):
	__tablename__ = 'Admins'
	id = Column(Integer, primary_key=True)
	username = Column(Text)
	password = Column(Text)

	def __init__(self):
		pass

Admins_Attrs = [
	'username',
	'password'
]

class Services(Base):
	__tablename__ = 'Services'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	type = Column(Integer)
	host = Column(Text)
	port = Column(Integer)
	email = Column(Text)
	
	def __init__(self, name, type, host, port, email):
		self.name = name
		self.type = type
		self.host = host
		self.port = port
		self.email = email

Services_Attrs = [
	'name',
	'type',
	'host',
	'port',
	'email'
]
