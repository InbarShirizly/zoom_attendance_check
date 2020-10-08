from flask_restful import fields
from server.models.custom_fields import StudentItemField, StatusItemField, UnixTimeStamp

# Fields for classrom.py
classrooms_list_fields = { # Fields list of classrooms
	'name': fields.String,
	'id': fields.Integer
}
classroom_resource_fields = { # Fields for a single classroom 
	'name': fields.String,
	'id': fields.Integer,
	'students': fields.List(StudentItemField)
}

# Fields for report.py
reports_list_fields = { # Fields list of classrooms
	'description': fields.String,
	'time': UnixTimeStamp(attribute="report_time"),
	'id': fields.Integer
}
report_resource_field = {
	'description': fields.String,
	'id': fields.Integer,
	'time': UnixTimeStamp(attribute="report_time"),
	'student_statuses': fields.List(StatusItemField)
}