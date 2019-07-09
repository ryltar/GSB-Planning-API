from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def doctor_queries():
    """ Gets an instance of 'DoctorQueries' from the 'g' environment. """
    if not hasattr(g, 'doc_queries'):
        g.doc_queries = DoctorQueries()
    return g.doc_queries


def parse_emp_args():
   """ Returns the employee's id in parameter, -1 if nothing. """
   if 'employee' not in request.args:
       return -1
   return request.args['employee']


class DoctorQueries:
    """ Manager for Doctor entity related SQL queries. """
    
    def get_doc_by_id(self):
        """ Returns a 'SELECT' query for a single Doctor. """
        return "SELECT * FROM doctor WHERE id = %s"

    def del_doc_by_id(self):
        """ Returns a 'DELETE' query for a single Doctor. """
        return "DELETE FROM doctor WHERE id = %s"

    def get_docs(self):
        """ Returns a 'SELECT' query for a single Doctor. """
        return "SELECT * FROM doctor"

    def post_doc(self):
        """ Returns an 'INSERT' query for a single Doctor. """
	return "INSERT INTO doctor(lastname, firstname, num_tel, email, id_address, id_employee, id_specialty) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id"

    def put_doc(self, key_list):
        """ Returns an 'UPDATE' query for a single Doctor. """
        tdoc = ""
        for k in range(len(key_list)):
            tdoc += key_list[k] + " = %s, "
	return "UPDATE doctor SET " + tdoc[:-2] + " WHERE id = %s"

    def get_emp_docs(self):
        """ Returns all doctors for a given employee. """
        return self.get_docs() + " WHERE id_employee = %s"


class Doctor(Resource):
    """ Flask_restful Resource for Doctor entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, doc_id):
        """ Returns a single Doctor. """
	query = doctor_queries().get_doc_by_id()
	doctor = get_service().get_content(query, [doc_id])
	if doctor is None:
            return jsonify(status=404)
        return jsonify(status=200,data=DoctorContainer(doctor).__dict__)

    @requires_admin_auth
    def delete(self, doc_id):
        """ Deletes a single Doctor. """
        query = doctor_queries().del_doc_by_id()
	value = get_service().del_content(query,[doc_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, doc_id):
        """ Edits a single Doctor. """
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(doc_id)
        query = doctor_queries().put_doc(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class DoctorContainer:
    """ The Doctor entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
        self.id = array[0]
    	self.lastname = array[1]
    	self.firstname = array[2]
	self.num_tel = array[3]
	self.email = array[4]
	self.id_address = array[5]
	self.id_employee = array[6]
	self.id_specialty = array[7]


class DoctorList(Resource):
    """ Flask_restful Resource for Doctor entity, for routes with no parameter."""

    @requires_admin_auth
    def get(self):
        """ Returns every single Doctor. """
	searched_emp = parse_emp_args()
        if searched_emp == -1:
            query = doctor_queries().get_docs()
	    doctors = get_service().get_contents(query)
	else:
	    query = doctor_queries().get_emp_docs()
	    doctors = get_service().get_custom_contents(query, [searched_emp])
	if doctors is None:
            return jsonify(status=404)
        json_to_return = []
        for e in doctors:
	    doc = DoctorContainer(e)
            json_to_return.append(doc.__dict__)
        return jsonify(status=201, data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Posts a single Doctor. """
        query = doctor_queries().post_doc()
	lastn = request.form['lastname']
	firstn = request.form['firstname']
	num = request.form['num_tel']
	email = request.form['email']
	add = request.form['id_address']
	emp = request.form['id_employee']
	spec = request.form['id_specialty']
	doc_id = get_service().post_content(query, [lastn, firstn, num, email, add, emp, spec])
	if doc_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=doc_id)
