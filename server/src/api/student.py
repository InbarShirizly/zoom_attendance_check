from flask_restful import Resource, abort, marshal_with_field, reqparse
from src.api import api
from src.models.orm import StudentModel
from src.config import RestErrors
from src.models.custom_fields import StudentItemField
from src import auth, db
from src.api.utils import validate_classroom

class StudentResource(Resource):
    """
    Resource responsible for student handling (get student information, change student's data)
    """
    method_decorators = [validate_classroom, auth.login_required]

    def __init__(self):
        super().__init__()
        self._put_args = reqparse.RequestParser()
        self._put_args.add_argument('name', type=str, location='json')
        self._put_args.add_argument('id_number', type=str, location='json')
        self._put_args.add_argument('org_class', type=str, location='json')
        self._put_args.add_argument('phone', type=str, location='json')
        self._put_args.add_argument('gender', type=bool, location='json')

    @marshal_with_field(StudentItemField)
    def get(self, class_id, student_id):
        """
        get information about the specific student in the classroom
        :param class_id: relevant classroom (checked in the "validate classroom decorator)
        :param student_id: id of student to present
        :return: student object from db
        """
        student = StudentModel.query.filter_by(id=student_id).first()
        if not student:
            abort(400, message=RestErrors.INVALID_STUDENT_ID)
        return student

    def put(self, class_id, student_id):
        """
        update student data - given arguments of data to update from the json request - will update data in the db
        :param class_id: relevant classroom (checked in the "validate classroom decorator)
        :param student_id: id of student to update
        :params - more params passing from the RequestParser of the user
                - more info about these in the init of in the api-doc
        :return:
        """
        student = StudentModel.query.filter_by(id=student_id)
        if not student.first():
            abort(400, message=RestErrors.INVALID_STUDENT_ID)

        args = self._put_args.parse_args(strict=True)
        args_without_none = {k: v for k, v in args.items() if v is not None} # Dropping arguments which werent given
        student.update(args_without_none)
        db.session.commit()
        return "", 204

        
api.add_resource(StudentResource, '/classrooms/<int:class_id>/students/<int:student_id>')