from flask_restful import fields


class StudentItemField(fields.Raw): # Custom field to parse StudentModel object
	def format(self, value):
		return {
			'id': value.id,
			'name': value.name,
			'id_number': value.id_number,
			'org_class': value.org_class,
			'gender': value.gender,
			'phone': value.phone
		}

class StatusItemField(fields.Raw): # Custom field to parse StatusModel
	def format(self, value):
		return {
			'status_id': value.id,
			'status': value.status,
			'student_name': value.student.name
		}

class UnixTimeStamp(fields.Raw): # Custom field to get time stamp
	def format(self, value):
		return value.timestamp()