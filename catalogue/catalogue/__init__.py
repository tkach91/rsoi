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
	
	
	## < 127.0.0.1:/catalogue_admin
	config.add_route('Auth_Admin_LOGOUT', '/logout_admin')
	config.add_route('Auth_Admin_LOGOIN', '/login_admin')
	
	config.add_route('Catalogue_Admin_INIT', '/catalogue_admin')
	config.add_route('Catalogue_Admin_CREATE', '/catalogue_admin/create')
	config.add_route('Catalogue_Admin_UPDATE', '/catalogue_admin/update')
	config.add_route('Catalogue_Admin_READ', '/catalogue_admin/read')
	config.add_route('Catalogue_Admin_DESTROY', '/catalogue_admin/destroy')
	
	config.add_route('Orders_Admin_CREATE', '/orders_admin/create')
	config.add_route('Orders_Admin_UPDATE', '/orders_admin/update')
	config.add_route('Orders_Admin_READ', '/orders_admin/read')
	config.add_route('Orders_Admin_DESTROY', '/orders_admin/destroy')
	## >
	
	
	## < 127.0.0.1:/catalogue
	config.add_route('Auth_SIGNIN', '/signin')
	config.add_route('Auth_LOGOUT', '/logout')
	config.add_route('Auth_LOGOIN', '/login')
	
	config.add_route('Catalogue_INIT', '/catalogue')
	config.add_route('Catalogue_CREATE', '/catalogue/create')
	config.add_route('Catalogue_UPDATE', '/catalogue/update')
	config.add_route('Catalogue_READ', '/catalogue/read')
	config.add_route('Catalogue_DESTROY', '/catalogue/destroy')
	
	config.add_route('Orders_CREATE', '/orders/create')
	config.add_route('Orders_UPDATE', '/orders/update')
	config.add_route('Orders_READ', '/orders/read')
	config.add_route('Orders_DESTROY', '/orders/destroy')
	
	config.add_route('Orders_Catalogue_CREATE', '/orders_catalogue/create')
	config.add_route('Orders_Catalogue_UPDATE', '/orders_catalogue/update')
	config.add_route('Orders_Catalogue_READ', '/orders_catalogue/read')
	config.add_route('Orders_Catalogue_DESTROY', '/orders_catalogue/destroy')
	## >
	
	
	config.scan()
	return config.make_wsgi_app()
