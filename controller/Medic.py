from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def medic_queries():
    """ Gets an instance of 'MedicQueries' from the 'g' environment. """
    if not hasattr(g, 'med_queries'):
        g.med_queries = MedicQueries()
    return g.med_queries


class MedicQueries:
    """ Manager for Medic entity related SQL queries. """

    def get_med_by_id(self):
        """ Returns a 'SELECT' query for a single Medic. """
        return "SELECT * FROM medic WHERE id = %s"

    def del_med_by_id(self):
        """ Returns a 'DELETE' query for a single Medic. """
        return "DELETE FROM medic WHERE id = %s"

    def get_meds(self):
        """ Returns a 'SELECT' query for a single Medic. """
        return "SELECT * FROM medic"

    def post_med(self):
        """ Returns an 'INSERT' query for a single Medic. """
	return "INSERT INTO medic(lib, description) VALUES(%s, %s) RETURNING id"

    def put_med(self, key_list):
        """ Returns an 'UPDATE' query for a single Medic. """
        tmed = ""
        for k in range(len(key_list)):
            tmed += key_list[k] + " = %s, "
	return "UPDATE medic SET " + tmed[:-2] + " WHERE id = %s"


class Medic(Resource):
    """ Flask_restful Resource for Medic entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, med_id):
        """ Returns a single Medic. """
        query = medic_queries().get_med_by_id()
	medic = get_service().get_content(query, [med_id])
	if medic is None:
            return jsonify(status=404)
        return jsonify(status=200,data=MedicContainer(medic).__dict__)

    @requires_admin_auth
    def delete(self, med_id):
        """ Deletes a single Medic. """
        query = medic_queries().del_med_by_id()
	value = get_service().del_content(query,[med_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, med_id):
        """ Edits a single Medic. """
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(med_id)
        query = medic_queries().put_med(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class MedicContainer:
    """ The Medic entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
    	self.id = array[0]
    	self.lib = array[1]
        self.description = array[2]


class MedicList(Resource):
    """ Flask_restful Resource for Medic entity, for routes with no parameter."""

    @requires_admin_auth
    def get(self):
        """ Returns every single Medic. """
        query = medic_queries().get_meds()
	medics = get_service().get_contents(query)
        if medics is None:
            return jsonify(status=404)
        json_to_return = []
        for e in medics:
	    med = MedicContainer(e)
            json_to_return.append(med.__dict__)
        return jsonify(data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Posts a single Medic. """
        query = medic_queries().post_med()
	lib = request.form['lib']
	desc = request.form['description']
	med_id = get_service().post_content(query, [lib, desc])
	if med_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=med_id)
