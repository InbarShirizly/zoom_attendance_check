from server.api import api
from flask_restful import Resource, reqparse, abort
from server import db, auth
from server.models.orm import StudentStatus
from server.config import RestErrors

STATUS_CHOICES = (0, 1, 2)

# arg parsing:

class StudentStatusResource(Resource):
    method_decorators = [auth.login_required]

    def __init__(self):
        super().__init__()

        self._put_args = reqparse.RequestParser()
        self._put_args.add_argument(
            'new_status', type=int,
            help=f"Bad choice, please pick one of this choices {STATUS_CHOICES}",
            required=True, location="json", choices=STATUS_CHOICES
        )

    def put(self, status_id):
        args = self._put_args.parse_args()
        status = StudentStatus.query.get(status_id)
        if status is None or status.report.classroom.teacher != auth.current_user():
            abort(400, message=RestErrors.INVALID_STATUS)

        status.status = args["new_status"]
        db.session.commit()

        return "", 204


api.add_resource(StudentStatusResource, '/status/<int:status_id>')
