from flask import jsonify, g, request, session, Response
from flask_restful import Resource
from strgen import StringGenerator
import jwt

from Service import *


def write_secret_to_file(id_num, secret):
    """ Puts the user's secret in a file. """
    fich = open(id_num + ".txt", "w")
    fich.write(secret)
    fich.close()


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def token_queries():
    """ Gets an instance of 'TokenQueries' from the 'g' environment. """
    if not hasattr(g, 'token_queries'):
        g.token_queries = TokenQueries()
    return g.token_queries


class TokenQueries:
    """ Manager for Toekn entity related SQL queries. """

    def get_emp_by_pass_and_mail(self):
	return "SELECT * FROM employee WHERE passwd = %s AND email = %s"


def generate_token(user):
    """ Generates a JWT for a user, according to the common standards. """
    secret = StringGenerator("[a-zA-Z1-9]{256}").render()
    header = {
        'alg' : 'HS256',
        'typ' : 'JWT'
    }
    payload = {
        'id' : str(user[0]),
        'name' : user[1] + ' ' + user[2],
        'admin': str(user[3])
    }
    token = jwt.encode(payload, secret, algorithm='HS256', headers=header)
    write_secret_to_file(str(user[0]), secret)
    return token


class Token(Resource):
    """ Flask_restful Resource for Token entity. """

    def post(self):
        """ Return a JWT for the user. """
	query = token_queries().get_emp_by_pass_and_mail()
	passwd = request.form['passwd']
	email = request.form['email']
	user = get_service().get_content(query, [passwd, email])	
	if user is not None:
	    token = generate_token(user)
	    return jsonify(status=201, token=token, employee_id=user[0])
        else:
            return jsonify(status=401, message="No user for those credentials.")

