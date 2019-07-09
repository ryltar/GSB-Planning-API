# coding: utf8

""" Signalization board for the app. Every route is defined here. """

from flask import *
from flask_restful import *

from Token import *

from Employee import *
from Doctor import *
from Medic import * 
from Appointment import *
from Address import *
from Specialty import *
from EmployeeAppointment import *
from IsMentioned import *

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

api = Api(app)

@app.route('/')
def hello():
    return "Bonjour"

# Route for authentication
api.add_resource(Token, '/auth/token')

# Routes for employees
api.add_resource(EmployeeList, '/admin/employees')
api.add_resource(Employee, '/admin/employees/<emp_id>')

# Routes for doctors
api.add_resource(DoctorList, '/admin/doctors')
api.add_resource(Doctor, '/admin/doctors/<doc_id>')

# Routes for medics
api.add_resource(MedicList, '/admin/medics')
api.add_resource(Medic, '/admin/medics/<med_id>')

# Routes for appointments
api.add_resource(AppointmentList, '/admin/appointments')
api.add_resource(Appointment, '/admin/appointments/<appoint_id>')

# Routes for addresses
api.add_resource(AddressList, '/admin/addresses')
api.add_resource(Address, '/admin/addresses/<addr_id>')

# Routes for specialties
api.add_resource(SpecialtyList, '/admin/specialties')
api.add_resource(Specialty, '/admin/specialties/<spec_id>')

# Routes for are_mentioned
api.add_resource(IsMentionedList, '/admin/medics-mentioned')
api.add_resource(IsMentioned, '/admin/medics-mentioned/<im_id>')

# Route for an employee's appointments
api.add_resource(EmployeeAppointmentList, '/admin/employee-appointment')
