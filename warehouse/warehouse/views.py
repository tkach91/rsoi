from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
	Session,
	)

from .models import (
	CatalogueOperator, CatalogueOperator_Attrs,
	)

from .lib import (
	CURD, authenticate, getUsername,
	)

from .smtp import  (
	WarehouseTransport,
	)

transport = WarehouseTransport.start()

@view_config(route_name='Warehouse_INIT', renderer='templates/Warehouse.pt')
def Warehouse_INIT(request):
	return ''

@view_config(route_name='Warehouse_CREATE', renderer='json')
def Warehouse_CREATE(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.create(CatalogueOperator, CatalogueOperator_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Warehouse_UPDATE', renderer='json')
def Warehouse_UPDATE(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.update(CatalogueOperator, CatalogueOperator_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Warehouse_READ', renderer='json')
def Warehouse_READ(request):
	data = CURD.read(CatalogueOperator, CatalogueOperator_Attrs)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Warehouse_DESTROY', renderer='json')
def Warehouse_DESTROY(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.destroy(CatalogueOperator, CatalogueOperator_Attrs, root)
	return {
		'root': data,
		'success': True
	}


