import os
from flask import g, request, Response, session
from functools import wraps
import jwt


def requires_basic_auth(f):
    """ Authorizes navigation in basic access pages. """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('authorization')
	    return Response(token)
	    num_id = jwt.decode(token, verify=False)['id']
	    return Response(num_id)
	    secret = read_secret_from_file(num_id)
	    payload = jwt.decode(token, secret)
	    return f(*args, **kwargs)
	except InvalidTokenError as e:
	    return Response('Exception : ' + e.msg, 401)
	except NoSecretFoundError as e:
	    return Response('Exception : ' + e.msg, 403)
        return no_token()
    return decorated


def requires_admin_auth(f):
    """ Authorizes navigation in admin access pages. """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('authorization')
	    num_id = jwt.decode(token, verify=False)['id']
	    secret = read_secret_from_file(num_id)
	    payload = jwt.decode(token, secret)
	    #if payload['admin']:
            return f(*args, **kwargs)
	    #return Response('You are not allowed to access this resource.', 401)
	except InvalidTokenError as e:
	    return Response('Exception : ' + e.msg, 401)
	except NoSecretFoundError as e:
	    return Response('Exception : ' + e.msg, 403)
    return decorated


def read_secret_from_file(num_id):
    """ Reads secret from the file corresponding to a user. """
    fich_ver = num_id + ".txt"
    if os.path.exists(fich_ver) and os.path.isfile(fich_ver):
        fich = open(fich_ver, "r")
	secret = fich.read()
	fich.close()
	return secret
    raise NoSecretFoundError()


class NoSecretFoundError(Exception):
    """Exception no secret file is found"""
    def __init__(self):
        self.msg = 'No secret found.'
