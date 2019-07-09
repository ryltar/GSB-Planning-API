from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def employee_queries():    
    """ Gets an instance of 'EmployeeQueries' from the 'g' environment. """
    if not hasattr(g, 'emp_queries'):
        g.emp_queries = EmployeeQueries()
    return g.emp_queries


class EmployeeQueries:
    """ Manager for Employee entity related SQL queries. """
    
    def get_emp_by_id(self):
        """ Returns a 'SELECT' query for a single Employee. """
        return "SELECT * FROM employee WHERE id = %s"

    def del_emp_by_id(self):
        """ Returns a 'DELETE' query for a single Employee. """
        return "DELETE FROM employee WHERE id = %s"

    def get_emps(self):
        """ Returns a 'SELECT' query for a single Employee. """
        return "SELECT * FROM employee"

    def post_emp(self):
        """ Returns an 'INSERT' query for a single Employee. """
	return "INSERT INTO employee(lastname, firstname, is_admin, passwd, email, num_tel, pseudo) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id"

    def put_emp(self, key_list):
        """ Returns an 'UPDATE' query for a single Employee. """
        temp = ""
        for k in range(len(key_list)):
            temp += key_list[k] + " = %s, "
	return "UPDATE employee SET " + temp[:-2] + " WHERE id = %s"


class Employee(Resource):
    """ Flask_restful Resource for Employee entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, emp_id):
        """ Returns a single Employee. """
        query = employee_queries().get_emp_by_id()
	employee = get_service().get_content(query, [emp_id])
	if employee is None:
            return jsonify(status=404)
        return jsonify(status=200,data=EmployeeContainer(employee).__dict__)

    @requires_admin_auth
    def delete(self, emp_id):
        """ Deletes a single Employee. """
        query = employee_queries().del_emp_by_id()
	value = get_service().del_content(query,[emp_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, emp_id):
        """ Edits a single Employee. """
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(emp_id)
        query = employee_queries().put_emp(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class EmployeeContainer:
    """ The Employee entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
        self.id = array[0]
    	self.lastname = array[1]
    	self.firstname = array[2]
        self.is_admin = array[3]
	self.passwd = array[4]
	self.email = array[5]
	self.num_tel = array[6]
	self.pseudo = array[7]


class EmployeeList(Resource):
    """ Flask_restful Resource for Employee entity, for routes with no parameter."""

    @requires_admin_auth
    def get(self):
        """ Returns every single Employee. """
        query = employee_queries().get_emps()
	employees = get_service().get_contents(query)
        if employees is None:
            return jsonify(status=404)
        json_to_return = []
        for e in employees:
	    emp = EmployeeContainer(e)
            json_to_return.append(emp.__dict__)
        return jsonify(data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Posts a single Employee. """
        query = employee_queries().post_emp()
	lastn = request.form['lastname']
	firstn = request.form['firstname']
	isadm = request.form['is_admin']
	pwd = request.form['passwd']
	email = request.form['email']
	num = request.form['num_tel']
	pseudo = request.form['pseudo']
	emp_id = get_service().post_content(query, [lastn, firstn, isadm, pwd, email, num, pseudo])
	if emp_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=emp_id)
