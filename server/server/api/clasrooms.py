from server.api import api
from flask_restful import Resource, reqparse, abort, marshal
from server import auth, db
from server.models.orm import TeacherModel, ClassroomModel
from werkzeug.datastructures import FileStorage
from server.parsing import parser
from server.parsing.utils import create_students_df
import pandas as pd
from server.config import RestErrors
from server.models.marshals import classrooms_list_fields, classroom_resource_fields


class ClassroomsResource(Resource):
	method_decorators = [auth.login_required]

	def __init__(self):
		super().__init__()
		
		self._post_args = reqparse.RequestParser(bundle_errors=True)
		self._post_args.add_argument('name', type=str, required=True)
		self._post_args.add_argument('students_file', type=FileStorage, location='files', help="Student file is required", required=True)
		
		self._put_args = reqparse.RequestParser(bundle_errors=True)
		self._put_args.add_argument('new_name', type=str, location="json", required=True)

	def get(self, class_id=None):
		if class_id is None:
			return marshal(auth.current_user().classrooms, classrooms_list_fields)

		current_class = ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message=RestErrors.INVALID_CLASS)
		return marshal(current_class, classroom_resource_fields)

	def post(self, class_id=None):
		if class_id:
			return abort(404, message=RestErrors.INVALID_ROUTE)
		args = self._post_args.parse_args()
		filename, stream = args['students_file'].filename.replace('"', ""), args['students_file'].stream  #TODO: replace here because of postman post request
		students_df = create_students_df(filename, stream)
		students = parser.parse_df(students_df)
		
		new_class = ClassroomModel(name=args['name'], teacher=auth.current_user())
		db.session.add(new_class)
		db.session.commit()

		students['class_id'] = pd.Series([new_class.id] * students.shape[0])
		students.to_sql('student', con=db.engine, if_exists="append", index=False)
		return {'class_id': new_class.id}

	def put(self, class_id=None):
		if class_id is None:
			return abort(404, message=RestErrors.INVALID_ROUTE)
		args = self._put_args.parse_args()
		current_class = ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message=RestErrors.INVALID_CLASS)
		current_class.name = args['new_name']
		db.session.commit()
		return "", 204

	def delete(self, class_id=None):
		if class_id is None: # Deleting all classes
			teacher_classes_id = db.session.query(ClassroomModel.id).filter_by(teacher=auth.current_user()).all()
			for class_data in teacher_classes_id:
				current_class = ClassroomModel.query.filter_by(id=class_data.id, teacher=auth.current_user()).first()
				db.session.delete(current_class)
			db.session.commit()
			return "", 204
		
		current_class = ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message=RestErrors.INVALID_CLASS)
		
		db.session.delete(current_class)
		db.session.commit()
		return "", 204

api.add_resource(ClassroomsResource, "/classrooms", "/classrooms/<int:class_id>") 