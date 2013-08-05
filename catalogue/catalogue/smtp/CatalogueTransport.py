#!/usr/bin/python
# -*- coding: utf-8

import time
import thread
import xmlrpclib
import poplib
import thread
import time
import base64
import simplejson as json
import transaction

from Email import Email

from sqlalchemy import create_engine
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
	scoped_session,
	sessionmaker,
	)
	
Engine = create_engine('postgresql+psycopg2://evg:evg@localhost/evg_1')
Session = sessionmaker(bind=Engine, extension=ZopeTransactionExtension())

Base = declarative_base()
Base.metadata.bind = Engine


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
	idCatalogue = Column(Integer)
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
	status = Column(Text)
	warehouses = Column(Integer, default=0)

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
	'password',
	'count'
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
	'password',
	'count'
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

# модуль обработки сообщений
# формирует xml-rpc сообщения, отправляет и принимает почту
# разбирает входящую почту по типу и источнику
class CatalogueTransport:
	def __init__(self):
		self.email = Email()

	# Добавление сервиса (склад/курьерская служба) в БД
	def add_service(self, name, type, host, port, email):
		session = Session()
		service = Services(name, type, host, port, email)
		session.add(service)
		session.flush()
		transaction.commit()

	# Отправка запроса на формирование заказа складам
	def warehouse_query(self, type, id, description, date):
		services = Session.query(Services).filter(Services.type==type).all()
		description = []
		orders_catalogue = Session.query(Orders_Catalogue).filter(Orders_Catalogue.idOrder==id).all()
		for order_catalogue in orders_catalogue:
			description.append({'idCatalogue':order_catalogue.idCatalogue, 'count':order_catalogue.count})

		json_description = json.dumps(description)
		i = 0
		for service in services:
			print "Sending mail to %s: %s..." % (service.name, service.email)
			content = 'id= %d; json_description= %s; date= %s' % (id, json_description, date)
			subject = 'warehouse_query %d' % id 
			self.email.sendmail(content, subject, [service.email])
			i += 1
		
		print
		print
		print
		print
		print
		print
		print
		print i
			
		order = Session.query(Orders).filter(Orders.id==id).first()
		order.status = 'accepted'
		order.warehouses = i
		transaction.commit()
		
	# Окончательный резерв заказа
	def accept_warehouse_query(self, type, id, service):
		content = 'id= %d' % id
		subject = 'accept_warehouse_query %d' % id 
		self.email.sendmail(content, subject, [service.email])
		
		order = Session.query(Orders).filter(Orders.id==id).first()
		order.status = 'reserverd'
		transaction.commit()

	# Отправка запроса на доставку заказа курьерской службе
	def postman_query(self, type, id, address, date):
		services = Session.query(Services).filter(Services.type==type).all()
		
		for service in services:
			print "Sending mail to %s: %s..." % (service.name, service.email)
			content = 'id= %d; address= %s; date= %s' % (id, address, date)
			subject = 'postman_query %d' % id 
			self.email.sendmail(content, subject, [service.email])

	# Окончательный резерв доставки
	def accept_postman_query(self, type, id, service):
		content = 'id= %d' % id
		subject = 'accept_query %d' % id 
		self.email.sendmail(content, subject, [service.email])
		
		order = Session.query(Orders).filter(Orders.id==id).first()
		order.status = 'delivering'
		transaction.commit()

	# Отмена заказа
	def cancel(self, type, id, service):
		content = 'id= %d' % id
		subject = 'cancel %d' % id
		self.email.sendmail(content, subject, [service.email])
		
		order = Session.query(Orders).filter(Orders.id==id).first()
		order.status = 'canceled'
		transaction.commit()

	def fetchmail(self):
		print "Fetching mail"
		mails = self.email.fetchmail()
		if mails:
			for mail in mails:
				print "EMAIL"
				print mail
				self.__new_mail__(mail)
				
	def __parse_email__(self, source):
		alist = source.split(' ')
		return alist[1]

	def __new_mail__(self, email):
		subject = email['subject']
		source = email['from']
		content = email['text']

		email = self.__parse_email__(source)
		print "MESSAGE from %s" % email
		
		dictionary = self.__get__(content)
	
		# Произведён пререзерв
		if (subject.startswith('Subject: warehouse_re_ok')):
			type = int(dictionary['type'])
			id = int(dictionary['id'])
			service = Session.query(Services).filter(Services.email==email).first()
			self.accept_warehouse_query(type, id, service)
		# Произведён резерв
		elif (subject.startswith('Subject: warehouse_re_reserved')):
			type = int(dictionary['type'])
			id = int(dictionary['id'])
			order = Session.query(Orders).filter(Orders.id==id).first()
			self.postman_query(1, id, order.address, order.date)
		elif (subject.startswith('Subject: warehouse_re_null')):
			type = int(dictionary['type'])
			id = int(dictionary['id'])
			order = Session.query(Orders).filter(Orders.id==id).first()
			order.warehouses = order.warehouses - 1
			if order.warehouses == 0:
				order.status = 'canceled'
			transaction.commit()
		elif (subject.startswith('Subject: postman_re_ok')):
			type = int(dictionary['type'])
			id = int(dictionary['id'])
			service = Session.query(Services).filter(Services.email==email).first()
			self.accept_postman_query(1, id, service)
		elif (subject.startswith('Subject: postman_re_delivering')):
			type = int(dictionary['type'])
			id = int(dictionary['id'])
			order = Session.query(Orders).filter(Orders.id==id).first()
			order.status = 'delivering'
			transaction.commit()
		elif (subject.startswith('Subject: postman_re_canceled')):
			type = int(dictionary['type'])
			id = int(dictionary['id'])
			order = Session.query(Orders).filter(Orders.id==id).first()
			order.status = 'canceled'
			transaction.commit()
		else:
			print "Invalid request '%s'." % subject
			
	def __get__(self, source):
		result = {}
		alist = source.split(';')

		for element in alist:
			element = element.strip()
			deuce = element.split(':')

			key = deuce[0].strip()
			value = deuce[1].strip()

			result[key] = value

		return result

def cycle():
	global transport
	global Session
	Session = Session()
	while True:
		transport.fetchmail()
		time.sleep(10.0)

def start():
	global transport

	transport = CatalogueTransport()
	thread.start_new_thread(cycle, ())
	return transport
