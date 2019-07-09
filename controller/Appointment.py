from flask import jsonify, g, request 
from flask_restful import Resource

from Authentication import *
from Service import *


def get_service():
    """ Gets an instance of 'Service' from the 'g' environment. """
    if not hasattr(g, 'service'):
        g.service = Service()
    return g.service


def appointment_queries():
    """ Gets an instance of 'AppointmentQueries' from the 'g' environment. """
    if not hasattr(g, 'appoint_queries'):
        g.appoint_queries = AppointmentQueries()
    return g.appoint_queries


class AppointmentQueries:
    """ Manager for Appointment entity related SQL queries. """
    
    def get_appoint_by_id(self):
        """ Returns a 'SELECT' query for a single Appointment. """
        query = "SELECT * FROM appointment a"
	query += " INNER JOIN is_mentioned i ON a.id = i.id_appointment"
	query += " WHERE id = %s"
	return query

    def del_appoint_by_id(self):
        """ Returns a 'DELETE' query for a single Appointment. """
        return "DELETE FROM appointment WHERE id = %s"

    def get_appoints(self):
        """ Returns a 'SELECT' query for a single Appointment. """
        return "SELECT * FROM appointment"

    def post_appoint(self):
        """ Returns an 'INSERT' query for a single Appointment. """
	return "INSERT INTO appointment(start_date, end_date, state, feedback, id_doctor) VALUES(%s, %s, %s, %s, %s) RETURNING id"

    def put_appoint(self, key_list):
        """ Returns an 'UPDATE' query for a single Appointment. """
        tappoint = ""
        for k in range(len(key_list)):
            tappoint += key_list[k] + " = %s, "
	return "UPDATE appointment SET " + tappoint[:-2] + " WHERE id = %s"


class Appointment(Resource):
    """ Flask_restful Resource for Appointment entity, for routes with a parameter. """

    @requires_admin_auth
    def get(self, appoint_id):
        """ Returns a single Appointment. """
        query = appointment_queries().get_appoint_by_id()
	appointment = get_service().get_content(query, [appoint_id])
	if appointment is None:
            return jsonify(status=404)
        return jsonify(status=200,data=AppointmentContainer(appointment).__dict__)

    @requires_admin_auth
    def delete(self, appoint_id):
        """ Deletes a single Appointment. """
        query = appointment_queries().del_appoint_by_id()
	value = get_service().del_content(query,[appoint_id])
        if value != 1:
            return jsonify(status=404)
        return jsonify(status=200)

    @requires_admin_auth
    def put(self, appoint_id):
        """ Edits a single Appointment. """
	key_list, value_list = [], []
        for key, value in request.form.items():
            key_list.append(key)
            value_list.append(value)
	value_list.append(appoint_id)
        query = appointment_queries().put_appoint(key_list)
	value = get_service().put_content(query, value_list)
	if value != 1:
            jsonify(status=404)
	return jsonify(status=200)


class AppointmentContainer:
    """ The Appointment entity itself. """
	
    def __init__(self, array):
        """ Builds the entity from a list. """
        self.id = array[0]
    	self.start_date = array[1]
    	self.end_date = array[2]
        self.state = array[3]
	self.feedback = array[4]
	self.id_doctor = array[5]


class AppointmentList(Resource):
    """ Flask_restful Resource for Appointment entity, for routes with no parameter."""

    @requires_admin_auth
    def get(self):
        """ Returns every single Appointment. """
        query = appointment_queries().get_appoints()
	appointments = get_service().get_contents(query)
        if appointments is None:
            return jsonify(status=404)
        json_to_return = []
        for e in appointments:
	    appoint = AppointmentContainer(e)
            json_to_return.append(appoint.__dict__)
        return jsonify(data=json_to_return)

    @requires_admin_auth
    def post(self):
        """ Posts a single Appointment. """
        query = appointment_queries().post_appoint()
	sdate = request.form['start_date']
	edate = request.form['end_date']
	state = request.form['state']
	feed = request.form['feedback']
	doc = request.form['id_doctor']
	appoint_id = get_service().post_content(query, [sdate, edate, state, feed, doc])
	if appoint_id == -1:
            return jsonify(status=404)
        return jsonify(status=200,data=appoint_id)
