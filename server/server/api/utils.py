from functools import wraps
from flask_restful import abort
from server import auth
from server.models.orm import ClassroomModel
from server import app
from server.config import RestErrors

# This decorator fucntion will make sure that the classroom belongs to the current user
def validate_classroom(fnc):
    def inner(class_id, report_id=None):
        if ClassroomModel.query.filter_by(id=class_id, teacher=auth.current_user()).first() is None:
            abort(400, message="Invalid class id")
        return fnc(class_id, report_id)
    return inner


# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return {"message": RestErrors.INVALID_ROUTE}