from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def address_queries():
    """ Gets an instance of 'AddressQueries' from the 'g' environment. """
    if not hasattr(g, 'addr_queries'):
        g.addr_queries = AddressQueries()
    return g.addr_queries


class AddressQueries:
    """ Manager for Address entity related SQL queries. """
    
    def get_addr_by_id(self):
        """ Returns a 'SELECT' query for a single Address. """
        return "SELECT * FROM address WHERE id = %s"

    def del_addr_by_id(self):
        """ Returns a 'DELETE' query for a single Address. """
        return "DELETE FROM address WHERE id = %s"

    def get_addrs(self):        
        """ Returns a 'SELECT' query for a single Address. """
        return "SELECT * FROM address"

    def post_addr(self):
        """ Returns an 'INSERT' query for a single Address. """
	return "INSERT INTO address(num, street, codepost, city, country, indication) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"

    def put_addr(self, key_list):
        """ Returns an 'UPDATE' query for a single Address. """
        taddr = ""
        for k in range(len(key_list)):
            taddr += key_list[k] + " = %s, "
	return "UPDATE address SET " + taddr[:-2] + " WHERE id = %s"


class Address(Resource):
    """ Flask_restful Resource for Address entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, addr_id):
        """ Returns a single Address. """
        query = address_queries().get_addr_by_id()
	address = get_service().get_content(query, [addr_id])
	if address is None:
            return jsonify(status=404)
        return jsonify(status=200,data=AddressContainer(address).__dict__)

    @requires_admin_auth
    def delete(self, addr_id):
        """ Deletes a single Address. """
        query = address_queries().del_addr_by_id()
	value = get_service().del_content(query,[addr_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, addr_id):
        """ Edits a single Address. """
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(addr_id)
        query = address_queries().put_addr(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class AddressContainer:
    """ The Address entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
        self.id = array[0]
    	self.num = array[1]
    	self.street = array[2]
        self.codepost = array[3]
	self.city = array[4]
	self.country = array[5]
	self.indication = array[6]


class AddressList(Resource):
    """ Flask_restful Resource for Address entity, for routes with no parameter."""

    @requires_admin_auth
    def get(self):
        """ Returns every single Address. """
        query = address_queries().get_addrs()
	addresss = get_service().get_contents(query)
        if addresss is None:
            return jsonify(status=404)
        json_to_return = []
        for e in addresss:
	    addr = AddressContainer(e)
            json_to_return.append(addr.__dict__)
        return jsonify(data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Posts a single Address. """
        query = address_queries().post_addr()
	num = request.form['num']
	street = request.form['street']
	codepost = request.form['codepost']
	city = request.form['city']
	country = request.form['country']
	indication = request.form['indication']
	addr_id = get_service().post_content(query, [num, street, codepost, city, country, indication])
	if addr_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=addr_id)
