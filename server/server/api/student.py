from flask_restful import Resource, abort, marshal_with_field, reqparse
from server.api import api
from server.models.orm import StudentModel
from server.config import RestErrors
from server.models.custom_fields import StudentItemField
from server import auth, db
from server.api.utils import validate_classroom

class StudentResource(Resource):
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
        student = StudentModel.query.filter_by(id=student_id).first()
        if not student:
            abort(400, message=RestErrors.INVALID_STUDENT_ID)
        return student

    def put(self, class_id, student_id):
        student = StudentModel.query.filter_by(id=student_id)
        if not student.first():
            abort(400, message=RestErrors.INVALID_STUDENT_ID)

        args = self._put_args.parse_args(strict=True)
        args_without_none = {k: v for k, v in args.items() if v is not None} # Dropping arguments which werent given
        student.update(args_without_none)
        db.session.commit()
        return "", 204

        
api.add_resource(StudentResource, '/classrooms/<int:class_id>/students/<int:student_id>')