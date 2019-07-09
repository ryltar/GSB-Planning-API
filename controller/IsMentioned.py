from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def is_mentioned_queries():
    """ Gets an instance of 'IsMentionedQueries' from the 'g' environment. """
    if not hasattr(g, 'im_queries'):
        g.im_queries = IsMentionedQueries()
    return g.im_queries


class IsMentionedQueries:    
    """ Manager for IsMentioned entity related SQL queries. """
    
    def get_im_by_id(self):
        """ Returns a 'SELECT' query for a single IsMentioned. """
        return "SELECT * FROM is_mentioned WHERE id = %s"

    def del_im_by_id(self):
        """ Returns a 'DELETE' query for a single IsMentioned. """
        return "DELETE FROM is_mentioned WHERE id = %s"

    def get_am(self):
        """ Returns a 'SELECT' query for a single IsMentioned. """
        return "SELECT * FROM is_mentioned"

    def post_im(self):
        """ Returns an 'INSERT' query for a single IsMentioned. """
	return "INSERT INTO is_mentioned(id, id_appointment) VALUES(%s, %s) RETURNING id"

    def put_im(self, key_list):
        """ Returns an 'UPDATE' query for a single IsMentioned. """
        tim = ""
        for k in range(len(key_list)):
            tim += key_list[k] + " = %s, "
	return "UPDATE is_mentioned SET " + tim[:-2] + " WHERE id = %s"


class IsMentioned(Resource):
    """ Flask_restful Resource for IsMentioned entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, im_id):
        """ Returns a single IsMentioned. """
        query = is_mentioned_queries().get_im_by_id()
	is_mentioned = get_service().get_content(query, [im_id])
	if is_mentioned is None:
            return jsonify(status=404)
        return jsonify(status=200,data=IsMentionedContainer(is_mentioned).__dict__)

    @requires_admin_auth
    def delete(self, im_id):
        """ Deletes a single IsMentioned. """
        query = is_mentioned_queries().del_im_by_id()
	value = get_service().del_content(query,[im_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, im_id):
        """ Edits a single IsMentioned. """        
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(im_id)
        query = is_mentioned_queries().put_im(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class IsMentionedContainer:
    """ The IsMentioned entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
    	self.id = array[0]
    	self.id_appointment = array[1]


class IsMentionedList(Resource):

    @requires_admin_auth
    def get(self):
        """ Flask_restful Resource for IsMentioned entity, for routes with no parameter."""
        query = is_mentioned_queries().get_am()
	are_mentioned = get_service().get_contents(query)
        if are_mentioned is None:
            return jsonify(status=404)
        json_to_return = []
        for e in are_mentioned:
	    im = IsMentionedContainer(e)
            json_to_return.append(im.__dict__)
        return jsonify(data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Returns every single IsMentioned. """
        query = is_mentioned_queries().post_im()
	idm = request.form['id']
	ida = request.form['id_appointment']
	im_id = get_service().post_content(query, [idm, ida])
	if im_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=im_id)
