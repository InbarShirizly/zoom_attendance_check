from flask_restful import fields
from server.models.custom_fields import StudentItemField

# Fields for classrom.py
classrooms_list_fields = { # Fields list of classrooms
	'name': fields.String,
	'id': fields.Integer
}
classroom_resource_fields = { # Fields for a single classroom 
	'name': fields.String,
	'students': fields.List(StudentItemField)
}

# Fields for report.py
reports_list_fields = { # Fields list of classrooms
	'description': fields.String,
	'id': fields.Integer
}
student_status_field = {
    'status': fields.Integer,
    'student_name': fields.String(attribute='student.name'),
    'status_id': fields.Integer(attribute="id")
}