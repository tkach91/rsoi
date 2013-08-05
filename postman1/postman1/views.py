from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
	Session,
	)

from .models import (
	Postman, Postman_Attrs,
	)

from .lib import (
	CURD, authenticate, getUsername,
	)


from .smtp import  (
	PostmanTransport,
	)

transport = PostmanTransport.start()

@view_config(route_name='PostMan_INIT', renderer='templates/POSTMan.pt')
def PostMan_INIT(request):
	return ''

@view_config(route_name='PostMan_CREATE', renderer='json')
def PostMan_CREATE(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.create(Postman, Postman_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='PostMan_UPDATE', renderer='json')
def PostMan_UPDATE(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.update(Postman, Postman_Attrs, root)
	
	print
	print
	print
	print data
	print
	if data[0]['status'] == 'accept':
		transport.postman_re_ok(data[0]['idExternal'])
	else:
		transport.postman_re_canceled(data[0]['idExternal'])
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='PostMan_READ', renderer='json')
def PostMan_READ(request):
	data = CURD.read(Postman, Postman_Attrs)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='PostMan_DESTROY', renderer='json')
def PostMan_DESTROY(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.destroy(Postman, Postman_Attrs, root)
	return {
		'root': data,
		'success': True
	}



