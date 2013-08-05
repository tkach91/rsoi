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

Engine = create_engine('postgresql+psycopg2://evg:evg@localhost/evg_4')
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

catalogue_email = 'mbox1727-00@dev.iu7.bmstu.ru'

class PostmanTransport:
	def __init__(self): 
		self.email = Email()

	# Даём положительный ответ
	def postman_re_ok(self, id):
		content = 'type: 1; id: %s' % (id.__str__()) 
		subject = 'postman_re_ok %s' % (id.__str__())
		self.email.sendmail(content, subject, [catalogue_email])

	# Подтверждаем доставку
	def postman_re_delivering(self, id):
		content = 'type: 1; id: %s' % (id.__str__()) 
		subject = 'postman_re_delivering %s' % (id.__str__())
		self.email.sendmail(content, subject, [catalogue_email])
		
	# Отказ в доставке
	def postman_re_canceled(self, id):
		content = 'type: 1; id: %s' % (id.__str__()) 
		subject = 'postman_re_canceled %s' % (id.__str__())
		self.email.sendmail(content, subject, [catalogue_email])

	def __new_mail__(self, email):
		if email['from'] == "From: %s" % catalogue_email:
			subject = email['subject']
			content = email['text']

			dictionary = self.__get__(content)
			print "have got dictionary:"
			if (subject.startswith('Subject: postman_query')):
				self.__reserve_order__(dictionary['id'], dictionary['address'], dictionary['date'])
			elif (subject.startswith('Subject: accept_postman_query')):
				postman = Session.query(Postman).filter(Postman.idExternal==dictionary['id']).first()
				postman.status = "delivering"
				transaction.commit()
			elif (subject.startswith('Subject: cancel')):
				self.__cancel_order__(dictionary[id])
			else:
				print "Invalid request '%s'." % subject
				
	def __reserve_order__(self, id, address, date):
		postman = Postman()
		postman.idExternal = id
		postman.address = address
		postman.date = date
		postman.status = "recieved"
		Session.add(postman)
		transaction.commit()
		
	def fetchmail(self):
		mails = self.email.fetchmail()
		if mails:
			for mail in mails:
				#print "EMAIL"
				#print mail
				self.__new_mail__(mail)
				
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

def __clear__():
	global transport
	
	while True:
		transport.fetchmail()
		
		time.sleep(10.0)
		
		print "Order clearing..."
		#postmans = Session.query(Postman).filter(Postman.status=="recieved").all()

		#for postman in postmans:
		#	print "Order %d has been deleted." % postman.id
		#	Session.delete(postman)
		#	transaction.commit()
		
		#time.sleep(30.0)
 
def start():
	global transport
	global Session
	Session = Session()
	transport = PostmanTransport()
	thread.start_new_thread(__clear__, ())
	return transport
