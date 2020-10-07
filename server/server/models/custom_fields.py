from flask_restful import fields


class StudentItemField(fields.Raw): # Custom field to parse StudentModel object
	def format(self, value):
		without_none = {k: v for k, v in value.__dict__ .items() if v is not None} # Getting only attributes which are not None
		del without_none['_sa_instance_state']
		del without_none['class_id']
		return without_none

class StatusItemField(fields.Raw): # Custom field to parse StatusModel
	def format(self, value):
		return {
			'status_id': value.id,
			'status': value.status,
			'student_name': value.student.name
		}