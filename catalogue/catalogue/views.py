from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
	Session,
	)

from .models import (
	Users, Users_Attrs,
	Admins, Admins_Attrs,
	Catalogue, Catalogue_Attrs,
	Orders, Orders_Attrs,
	Orders_Catalogue, Orders_Catalogue_Attrs,
	)

from .lib import (
	CURD, authenticate, getUsername,
	)

from .smtp import  (
	CatalogueTransport,
	)

transport = CatalogueTransport.start()


## < 127.0.0.1:/catalogue_admin
@view_config(route_name='Auth_SIGNIN', renderer='json')
def Auth_SIGNIN(request):
	username = None
	if 'username' in request.params:
		username = request.params['username']
		
	password = None
	if 'password' in request.params:
		password = request.params['password']
	
	newUser = [{'username':username, 'password':password}]
	CURD.create(Users, Users_Attrs, newUser)
	return 'ok'

@view_config(route_name='Auth_Admin_LOGOUT', renderer='json')
def Auth_Admin_LOGOUT(request):
	if 'idUser' in request.session:
		del request.session['idUser']
		del request.session['username']
	return 'ok'

@view_config(route_name='Auth_Admin_LOGOIN', renderer='json')
def Auth_Admin_LOGOIN(request):
	username = None
	if 'username' in request.params:
		username = request.params['username']
		
	password = None
	if 'password' in request.params:
		password = request.params['password']
	
	condition = (Admins.username == username) & (Admins.password == password)
	username_password = CURD.read(Admins, Admins_Attrs, condition)
	
	if username_password == []:
		Auth_LOGOUT(request)
		return 'no'
		
	request.session['username'] = username_password[0]['username']
	request.session['idUser'] = username_password[0]['id']
	return 'ok'


@view_config(route_name='Catalogue_Admin_INIT', renderer='templates/Catalogue_Admin.pt')
def Catalogue_Admin_INIT(request):
	return {'auth': authenticate(request.session), 'username': getUsername(request.session) }

@view_config(route_name='Catalogue_Admin_CREATE', renderer='json')
def Catalogue_Admin_CREATE(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.create(Catalogue, Catalogue_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Catalogue_Admin_UPDATE', renderer='json')
def Catalogue_Admin_UPDATE(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.update(Catalogue, Catalogue_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Catalogue_Admin_READ', renderer='json')
def Catalogue_Admin_READ(request):
	data = CURD.read(Catalogue, Catalogue_Attrs)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Catalogue_Admin_DESTROY', renderer='json')
def Catalogue_Admin_DESTROY(request):
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.destroy(Catalogue, Catalogue_Attrs, root)
	return {
		'root': data,
		'success': True
	}


@view_config(route_name='Orders_Admin_CREATE', renderer='json')
def Orders_Admin_CREATE(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	
	data = CURD.create(Orders, Orders_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_Admin_UPDATE', renderer='json')
def Orders_Admin_UPDATE(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.update(Orders, Orders_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_Admin_READ', renderer='json')
def Orders_Admin_READ(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	data = CURD.read(Orders, Orders_Attrs)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_Admin_DESTROY', renderer='json')
def Orders_Admin_DESTROY(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.destroy(Orders, Orders_Attrs, root)
	return {
		'root': data,
		'success': True
	}
## 127.0.0.1:/catalogue_admin >



## < 127.0.0.1:/catalogue

@view_config(route_name='Auth_LOGOUT', renderer='json')
def Auth_LOGOUT(request):
	if 'idUser' in request.session:
		del request.session['idUser']
		del request.session['username']
	return 'ok'

@view_config(route_name='Auth_LOGOIN', renderer='json')
def Auth_LOGOIN(request):
	username = None
	if 'username' in request.params:
		username = request.params['username']
		
	password = None
	if 'password' in request.params:
		password = request.params['password']
	
	condition = (Users.username == username) & (Users.password == password)
	username_password = CURD.read(Users, Users_Attrs, condition)
	if username_password == []:
		Auth_LOGOUT(request)
		return 'no'
		
	request.session['username'] = username_password[0]['username']
	request.session['idUser'] = username_password[0]['id']
	return 'ok'


@view_config(route_name='Catalogue_INIT', renderer='templates/Catalogue.pt')
def Catalogue_INIT(request):
	return {'auth': authenticate(request.session), 'username': getUsername(request.session) }

@view_config(route_name='Catalogue_READ', renderer='json')
def Catalogue_READ(request):
	data = CURD.read(Catalogue, Catalogue_Attrs)
	return {
		'root': data,
		'success': True
	}


@view_config(route_name='Orders_CREATE', renderer='json')
def Orders_CREATE(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	
	for i in root:
		i['idUser'] = request.session['idUser']
		
	data = CURD.create(Orders, Orders_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_UPDATE', renderer='json')
def Orders_UPDATE(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.update(Orders, Orders_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_READ', renderer='json')
def Orders_READ(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	condition_ = Orders.idUser == request.session['idUser']
	data = CURD.read(Orders, Orders_Attrs, condition=condition_)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_DESTROY', renderer='json')
def Orders_DESTROY(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.destroy(Orders, Orders_Attrs, root)
	return {
		'root': data,
		'success': True
	}


@view_config(route_name='Orders_Catalogue_CREATE', renderer='json')
def Orders_Catalogue_CREATE(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	
	if type(root) != type([]):
		root = [root]
	data = CURD.create(Orders_Catalogue, Orders_Catalogue_Attrs, root)
	condition_ = Orders.id == data[0]['idOrder']
	order = CURD.read(Orders, Orders_Attrs, condition=condition_)
	transport.warehouse_query(0, order[0]['id'], '', order[0]['date'])
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_Catalogue_UPDATE', renderer='json')
def Orders_Catalogue_UPDATE(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.update(Orders_Catalogue, Orders_Catalogue_Attrs, root)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_Catalogue_READ', renderer='json')
def Orders_Catalogue_READ(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	condition_ = True
	if 'fakeLoad' in request.params:
		condition_ = False
		
	if 'idOrder' in request.params:
		idOrder = int (request.params['idOrder'])
		condition_ = Orders_Catalogue.idOrder == idOrder
	data = CURD.read(Orders_Catalogue, Orders_Catalogue_Attrs, condition=condition_)
	return {
		'root': data,
		'success': True
	}

@view_config(route_name='Orders_Catalogue_DESTROY', renderer='json')
def Orders_Catalogue_DESTROY(request):
	if not(authenticate(request.session)):
		return {
			'root': [],
			'success': True
		}
	root = request.json_body['root']
	if type(root) != type([]):
		root = [root]
	data = CURD.destroy(Orders_Catalogue, Orders_Catalogue_Attrs, root)
	return {
		'root': data,
		'success': True
	}
## 127.0.0.1:/catalogue >

