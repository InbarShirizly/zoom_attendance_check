from Server.api import api
from flask_restful import Resource, reqparse, abort, fields, marshal
from Server import auth, db
from Server.models import TeacherModel, ClassroomModel
from werkzeug.datastructures import FileStorage
from Server.utils import parser
from Server.utils.utils import create_students_df
import pandas as pd

# Fields:
classrooms_list_fields = { # Fields list of classrooms
	'name': fields.String,
	'id': fields.Integer
}
class StudentItemField(fields.Raw): # Custom field to parse StudentModel object

	def format(self, value):
		without_none = {k: v for k, v in value.__dict__ .items() if v is not None} # Getting only attributes which are not None
		del without_none['_sa_instance_state']
		return without_none

classroom_resource_fields = { # Fields for a single classroom 
	'name': fields.String,
	'students': fields.List(StudentItemField)
}


# arg parsing:
classrooms_post_argparse = reqparse.RequestParser()
classrooms_post_argparse.add_argument('name', type=str, help="Name of the class is required", required=True)
classrooms_post_argparse.add_argument('students_file', type=FileStorage, location='files', help="Student file is required", required=True)


class ClassroomsResource(Resource):
	method_decorators = [auth.login_required]

	def get(self, class_id=None):
		if class_id is None:
			return marshal(auth.current_user().classrooms, classrooms_list_fields)

		current_class = ClassroomModel.query.filter_by(id=class_id, teacher_model=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message="Invalid class id")
		return marshal(current_class, classroom_resource_fields)

	def post(self, class_id=None):
		if class_id:
			return abort(404, message="Invalid route")
		args = classrooms_post_argparse.parse_args()
		filename, stream = args['students_file'].filename.replace('"', ""), args['students_file'].stream  #TODO: replace here because of postman post request
		students_df = create_students_df(filename, stream)
		students = parser.parse_df(students_df)
		
		new_class = ClassroomModel(name=args['name'], teacher_model=auth.current_user())
		db.session.add(new_class)
		db.session.commit()

		students['class_id'] = pd.Series([new_class.id] * students.shape[0])
		students.to_sql('student_model', con=db.engine, if_exists="append", index=False)
		return "", 200

	def delete(self, class_id=None):
		if class_id is None: # Deleting all classes
			teacher_classes_id = db.session.query(ClassroomModel.id).filter_by(teacher_model=auth.current_user()).all()
			for class_data in teacher_classes_id:
				current_class = ClassroomModel.query.filter_by(id=class_data.id, teacher_model=auth.current_user()).first()
				db.session.delete(current_class)
			db.session.commit()
			return "", 204
		
		current_class = ClassroomModel.query.filter_by(id=class_id, teacher_model=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message="Invalid class id")
		
		db.session.delete(current_class)
		db.session.commit()
		return "", 204

api.add_resource(ClassroomsResource, "/classrooms", "/classrooms/<int:class_id>") 