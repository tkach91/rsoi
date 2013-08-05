from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
	sessionmaker,
	)
from zope.sqlalchemy import ZopeTransactionExtension
import models

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	session_factory = UnencryptedCookieSessionFactoryConfig('generadordesecretosparasessionesabiertasycerradas')
	
	models.Engine = engine_from_config(settings, 'sqlalchemy.')
	models.Session = sessionmaker(bind=models.Engine, extension=ZopeTransactionExtension())
	models.Base.metadata.bind = models.Engine
	
	config = Configurator(settings=settings, session_factory = session_factory)
	config.add_static_view('static', 'static', cache_max_age=3600)
	
	## < 127.0.0.1:/postman
	config.add_route('PostMan_CREATE', '/postman/create')
	config.add_route('PostMan_UPDATE', '/postman/update')
	config.add_route('PostMan_READ', '/postman/read')
	config.add_route('PostMan_DESTROY', '/postman/destroy')
	config.add_route('PostMan_INIT', '/postman')
	## >
	
	config.scan()
	return config.make_wsgi_app()
