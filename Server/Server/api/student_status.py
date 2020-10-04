from Server.api import api
from flask_restful import Resource, reqparse, abort
from Server import db, auth
from Server.models import StudentStatus

STATUS_CHOICES = (0, 1, 2)

# arg parsing:
student_status_argparse = reqparse.RequestParser()
student_status_argparse.add_argument('new_status', type=int,
                                     help=f"Bad choice, please pick one of this choices {STATUS_CHOICES}",
                                     required=True, location="json", choices=STATUS_CHOICES)

class StudentStatusResource(Resource):
    method_decorators = [auth.login_required]

    def put(self, status_id):
        args = student_status_argparse.parse_args()
        status = StudentStatus.query.get(status_id)
        if status is None or status.report.classroom.teacher != auth.current_user():
            abort(400, message="Invalid status id")

        status.status = args["new_status"]
        db.session.commit()

        return "", 204


api.add_resource(StudentStatusResource, '/status/<int:status_id>')
