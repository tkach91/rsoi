
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


class CatalogueOperator(Base):
	__tablename__ = 'Catalogue'
	id = Column(Integer, primary_key=True)
	idCatalogue = Column(Integer, unique=True)
	name = Column(Text)
	description = Column(Text)
	price = Column(Float)
	count = Column(Integer)

	def __init__(self):
		pass

CatalogueOperator_Attrs = [
	'idCatalogue',
	'name',
	'description',
	'price',
	'count'
]

class OrdersOperator(Base):
	__tablename__ = 'Orders'
	id = Column(Integer, primary_key=True)
	date = Column(Date)
	status = Column(Text)

	def __init__(self):
		pass

OrdersOperator_Attrs = [
	'idUser',
	'address',
	'date',
	'status'
]

class Orders_Catalogue(Base):
	__tablename__ = 'Orders_Catalogue'
	id = Column(Integer, primary_key=True)
	idOrder = Column(Integer)
	idCatalogue = Column(Integer)
	count = Column(Integer)

	def __init__(self):
		pass

Orders_Catalogue_Attrs = [
	'idOrder',
	'idCatalogue',
	'count'
]
