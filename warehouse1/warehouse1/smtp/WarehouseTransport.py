#!/usr/bin/python
#! coding: utf-8

import time
import os
import thread
import base64
import os
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

Engine = create_engine('postgresql+psycopg2://evg:evg@localhost/evg_2')
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

class CatalogueOperator(Base):
	__tablename__ = 'Catalogue'
	id = Column(Integer, primary_key=True)
	idCatalogue = Column(Integer)
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

class Orders_CatalogueOperator(Base):
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

catalogue_email = 'mbox1727-00@dev.iu7.bmstu.ru'

class WarehouseTransport:
	def __init__(self): 
		self.email = Email()

	# Даём положительный ответ
	def warehouse_re_ok(self, id):
		content = 'type: 0; id: %s' % (id.__str__()) 
		subject = 'warehouse_re_ok %s' % (id.__str__())
		self.email.sendmail(content, subject, [catalogue_email])

	# Подтверждаем резервирование
	def warehouse_re_reserved(self, id):
		content = 'type: 0; id: %s' % (id.__str__()) 
		subject = 'warehouse_re_reserved %s' % (id.__str__())
		self.email.sendmail(content, subject, [catalogue_email])
		
	# Невозможно укомплектовать заказ
	def warehouse_re_null(self, id):
		content = 'type: 0; id: %s' % (id.__str__()) 
		subject = 'warehouse_re_null %s' % (id.__str__())
		self.email.sendmail(content, subject, [catalogue_email])

	def __new_mail__(self, email):
		if email['from'] == "From: %s" % catalogue_email:
			subject = email['subject']
			content = email['text']

			dictionary = self.__get__(content)
			print "have got dictionary:"
			if (subject.startswith('Subject: warehouse_query')):
				self.__reserve_order__(dictionary['id'], dictionary['json_description'], dictionary['date'])  
			elif (subject.startswith('Subject: accept_warehouse_query')):
				order = Session.query(OrdersOperator).filter(OrdersOperator.id==dictionary['id']).first()
				order.status = "reserved"
				transaction.commit()
				self.warehouse_re_reserved(dictionary['id'])
			elif (subject.startswith('Subject: cancel')):
				self.__cancel_order__(dictionary[id])
			else:
				print "Invalid request '%s'." % subject
				
	def fetchmail(self):
		mails = self.email.fetchmail()
		if mails:
			for mail in mails:
				#print "EMAIL"
				#print mail
				self.__new_mail__(mail)

	# Резверв
	def __reserve_order__(self, id, json_description, date):
		description = json.loads(json_description)

		date = date.replace('T', '')
		for order in description:
			check = Session.query(CatalogueOperator).filter((CatalogueOperator.idCatalogue==order['idCatalogue']) & (CatalogueOperator.count>=int(order['count']))).first()
			if check == None:
				print "Tak"
				# Engine.rollback()
				self.warehouse_re_null(id)
				return
			
			newOrder = Orders_CatalogueOperator()
			newOrder.count = order['count']
			newOrder.idCatalogue = order['idCatalogue']
			newOrder.idOrder = id
			
			check.count -= order['count']
			Session.add(newOrder)
		
		order = OrdersOperator()
		order.id = id
		order.status = "prereserved"
		order.date = date
		Session.add(order)
		transaction.commit()
		
		self.warehouse_re_ok(id)

	# Отмена заказа
	def __cancel_order__(self, id):
		orders = Session.query(Orders_CatalogueOperator).filter(Orders_CatalogueOperator.idOrder==id).all()
		for order in orders:
			Session.delete(order)
			transaction.commit()
			
		order = Session.query(OrdersOperator).filter(OrdersOperator.id==id).first()
		order.status = "canceled"
		transaction.commit()

	def __get__(self, source):
		result = {}
		alist = source.split(';')

		for element in alist:
			element = element.strip()
			deuce = element.split('=')

			key = deuce[0].strip()
			value = deuce[1].strip()

			result[key] = value

		return result

def __deliver__():
	global transport
	
	while True:
		transport.fetchmail()
		
		time.sleep(5)
		
def __clear__():
	global transport
	
	while True:
		print "Order clearing..."
		orders = Session.query(OrdersOperator).filter(OrdersOperator.status == 'prereserved').all()

		for order in orders:
			print "Order %d has been deleted." % order.id
			orders_catalogue = Session.query(Orders_CatalogueOperator).filter(Orders_CatalogueOperator.idOrder == order.id).all()
			for order_catalogue in orders_catalogue:
				check = Session.query(CatalogueOperator).filter(CatalogueOperator.idCatalogue==order_catalogue.idCatalogue).first()
				check.count += order_catalogue.count
				Session.delete(order_catalogue)
				
			Session.delete(order)
			transaction.commit()
		
		time.sleep(40.0)
 
def start():
	global transport
	global Session
	Session = Session()
	transport = WarehouseTransport()
	thread.start_new_thread(__deliver__, ())
	thread.start_new_thread(__clear__, ())
	return transport
