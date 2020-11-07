from src.api import api, custom_types
from flask_restful import Resource, reqparse, abort, marshal, marshal_with
from src import auth, db
from src.models.orm import TeacherModel, ClassroomModel
import pandas as pd
from src.config import RestErrors, ValidatorsConfig
from src.models.marshals import classrooms_list_fields, classroom_resource_fields


class ClassroomsResource(Resource):
	"""
	Resource responsible for class handling (creating new class, getting class information, deleting class and more)
	"""
	method_decorators = [auth.login_required]

	def __init__(self):
		super().__init__()
		
		self._post_args = reqparse.RequestParser(bundle_errors=True)
		self._post_args.add_argument('name', type=str, required=True)
		self._post_args.add_argument('students_file', type=custom_types.students_file, location='files', required=True, dest="student_df")
		
		self._put_args = reqparse.RequestParser(bundle_errors=True)
		self._put_args.add_argument('new_name', type=str, location="json", required=True)

	def get(self, class_id=None):
		"""
		The function will get information about all classes or full information about specific class of a user
		param is given via the url
		:param class_id: the class id, or None for all classes (int)
		:return: information about the requested data (json) - for the object parsing check src.models.custom_fields, src.models.marshals
		"""
		if class_id is None:
			return marshal(auth.current_user().classrooms, classrooms_list_fields)

		current_class = ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message=RestErrors.INVALID_CLASS)
		return marshal(current_class, classroom_resource_fields)

	@marshal_with(classroom_resource_fields)
	def post(self, class_id=None):
		"""
		The function will create new classroom
		given from url:
		:param class_id: always must be None, must be giving due the init of the endpoint, 404 error will be raised if not None
		params are given in form data of the post request, check src.api.validators for full types:
		:param name: the name of the classroom (str)
		:param student_df: the file of the students - converted to df (custom_types.students_file)
		:return: information about the new classroom (json) - for the object parsing check src.models.custom_fields, src.models.marshals
		"""
		if class_id:
			abort(404, message=RestErrors.INVALID_ROUTE)
		if len(auth.current_user().classrooms) >= ValidatorsConfig.MAX_CLASSROOMS:
			abort(400, message=RestErrors.MAX_CLASSROOMS)

		args = self._post_args.parse_args()
	
		new_class = ClassroomModel(name=args['name'], teacher=auth.current_user())
		db.session.add(new_class)
		db.session.commit()

		args['student_df']['class_id'] = pd.Series([new_class.id] * args['student_df'].shape[0])
		args['student_df'].to_sql('student', con=db.engine, if_exists="append", index=False)
		return new_class

	def put(self, class_id=None):
		"""
		The function will change the name of the classroom
		given from url:
		:param class_id: always must be None, must be giving due the init of the endpoint, 404 error will be raised if not None
		other param is given in json format
		:param new_name: the new name of the classroom (str)
		:return: 204 http code if succeeded
		"""
		if class_id is None:
			abort(404, message=RestErrors.INVALID_ROUTE)
		args = self._put_args.parse_args()
		current_class = ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() # Making sure the class belongs to the current user
		if current_class is None:
			abort(400, message=RestErrors.INVALID_CLASS)
		current_class.name = args['new_name']
		db.session.commit()
		return "", 204

	def delete(self, class_id=None):
		"""
		The function will delete specific classroom or all classrooms of the user
		given from url:
		:param class_id: the class to delete, if None deletes all classes
		:return: 204 http code if succeeded 
		"""
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