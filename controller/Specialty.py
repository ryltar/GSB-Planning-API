from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def specialty_queries():
    """ Gets an instance of 'SpecialtyQueries' from the 'g' environment. """
    if not hasattr(g, 'spec_queries'):
        g.spec_queries = SpecialtyQueries()
    return g.spec_queries


class SpecialtyQueries:    
    """ Manager for Specialty entity related SQL queries. """
    
    def get_spec_by_id(self):
        """ Returns a 'SELECT' query for a single Specialty. """
        return "SELECT * FROM specialty WHERE id = %s"

    def del_spec_by_id(self):
        """ Returns a 'DELETE' query for a single Specialty. """
        return "DELETE FROM specialty WHERE id = %s"

    def get_specs(self):
        """ Returns a 'SELECT' query for a single Specialty. """
        return "SELECT * FROM specialty"

    def post_spec(self):
        """ Returns an 'INSERT' query for a single Specialty. """
	return "INSERT INTO specialty(label) VALUES(%s) RETURNING id"

    def put_spec(self, key_list):
        """ Returns an 'UPDATE' query for a single Specialty. """
        tspec = ""
        for k in range(len(key_list)):
            tspec += key_list[k] + " = %s, "
	return "UPDATE specialty SET " + tspec[:-2] + " WHERE id = %s"


class Specialty(Resource):
    """ Flask_restful Resource for Specialty entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, spec_id):
        """ Returns a single Specialty. """
        query = specialty_queries().get_spec_by_id()
	specialty = get_service().get_content(query, [spec_id])
	if specialty is None:
            return jsonify(status=404)
        return jsonify(status=200,data=SpecialtyContainer(specialty).__dict__)

    @requires_admin_auth
    def delete(self, spec_id):
        """ Deletes a single Specialty. """
        query = specialty_queries().del_spec_by_id()
	value = get_service().del_content(query,[spec_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, spec_id):
        """ Edits a single Specialty. """        
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(spec_id)
        query = specialty_queries().put_spec(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class SpecialtyContainer:
    """ The Specialty entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
    	self.id = array[0]
    	self.label = array[1]


class SpecialtyList(Resource):

    @requires_admin_auth
    def get(self):
        """ Flask_restful Resource for Specialty entity, for routes with no parameter."""
        query = specialty_queries().get_specs()
	specialties = get_service().get_contents(query)
        if specialties is None:
            return jsonify(status=404)
        json_to_return = []
        for e in specialties:
	    spec = SpecialtyContainer(e)
            json_to_return.append(spec.__dict__)
        return jsonify(data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Returns every single Specialty. """
        query = specialty_queries().post_spec()
	label = request.form['label']
	spec_id = get_service().post_content(query, [label])
	if spec_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=spec_id)
