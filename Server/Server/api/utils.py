from functools import wraps
from flask_restful import abort
from Server import auth
from Server.models import ClassroomModel

# This decorator fucntion will make sure that the classroom belongs to the current user
def validate_classroom(fnc):
    def inner(class_id, report_id=None):
        if ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() is None:
            abort(400, message="Invalid class id")
        return fnc(self, class_id, report_id)
    return inner