from functools import wraps
from flask_restful import abort
from server import auth
from server.models.orm import ClassroomModel, TeacherModel
from server import app
from server.config import RestErrors, SerializeConfig
from server.api import login_token_serializer
from itsdangerous.exc import BadSignature, BadTimeSignature

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


# Token validator for the authentication
@auth.verify_token
def verify_user_token(token):
    try:
        user_id = login_token_serializer.loads(token, max_age=SerializeConfig.LOIGN_TOKEN_AGE)
        return TeacherModel.query.get(user_id)
    except BadTimeSignature:
        abort(401, message=RestErrors.TOKEN_EXPIRED)
    except BadSignature:
        abort(401, message=RestErrors.INVALID_TOKEN)