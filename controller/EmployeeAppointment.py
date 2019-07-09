from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def emp_appointment_queries():
    """ Gets an instance of 'EmployeeAppointmentQueries' from the 'g' environment. """
    if not hasattr(g, 'emp_appoint_queries'):
        g.emp_appoint_queries = EmployeeAppointmentQueries()
    return g.emp_appoint_queries


def parse_state_args():
    """ Returns the state of the searched appointments, -1 if all are searched. """
    if 'state' in request.args:
        if request.args['state'] == 'future':
	    return 0
	elif request.args['state'] == 'unvalidated':
	    return 1
	elif request.args['state'] == 'archived':
	    return 2
    else:
	return -1


class EmployeeAppointmentQueries:
    """ Manager for EmployeeAppointment entity related SQL queries. """
    
    def get_all_appoints(self):
        """ Returns a 'SELECT' query for EmployeeAppointment. """
        query = "SELECT * FROM appointment ap"
	query += " INNER JOIN doctor d ON ap.id_doctor = d.id"
	query += " INNER JOIN address ad ON d.id_address = ad.id"
	query += " LEFT OUTER JOIN specialty s ON d.id_specialty = s.id"
	query += " WHERE d.id_employee = %s"
	return query
 
    def get_cust_appoints(self):
        """ Returns a 'SELECT' query for EmployeeAppointment. """
	return self.get_all_appoints() + " AND ap.state = %s"


class EmployeeAppointmentContainer:
    """ The EmployeeAppointment entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
        self.id = array[0]
    	self.start_date = array[1]
    	self.end_date = array[2]
	self.state = array[3]
	self.feedback = array[4]
	self.id_doctor = array[5]
	self.lastname_doctor = array[7]
	self.firstname_doctor = array[8]
	self.num_tel_doctor = array[9]
	self.email_doctor = array[10]
	self.id_address = array[11]
	self.num_address = array[15]
	self.street_address = array[16]
	self.codepost_address = array[17]
	self.city_address = array[18]
	self.country_address = array[19]
	self.indication_address = array[20]
	self.id_specialty = array[21]
	self.label_specialty = array[22]


class EmployeeAppointmentList(Resource):
    """ Flask_restful Resource for EmployeeAppointment entity, for routes with no parameter."""

    @requires_admin_auth
    def post(self):
        """ Returns every single EmployeeAppointment of the requested user. """
        query_params = [request.form['id_employee']]
	appointment_state = parse_state_args()
        if appointment_state == -1:
            query = emp_appointment_queries().get_all_appoints()
        else:
	    query = emp_appointment_queries().get_cust_appoints()
	    query_params.append(str(appointment_state))
        appointments = get_service().get_custom_contents(query, query_params)
	if appointments is None:
            return jsonify(status=404)
        json_to_return = []
        for e in appointments:
	    appoint = EmployeeAppointmentContainer(e)
            json_to_return.append(appoint.__dict__)
        return jsonify(status=200, data=json_to_return)

