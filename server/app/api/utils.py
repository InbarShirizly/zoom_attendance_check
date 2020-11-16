from functools import wraps
from flask_restful import abort
from app import auth
from app.models.orm import ClassroomModel, TeacherModel
from app import app
from app.config import RestErrors, SerializeConfig
from app.api import login_token_serializer
from itsdangerous.exc import BadSignature, BadTimeSignature


# This decorator function will make sure that the classroom belongs to the current user
def validate_classroom(fnc):
    def inner(*args, **kwargs):
        if ClassroomModel.query.filter_by(id=kwargs['class_id'], teacher=auth.current_user()).first() is None:
            abort(400, message=RestErrors.INVALID_CLASS)
        return fnc(*args, **kwargs)
    return inner


# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return {"message": RestErrors.INVALID_ROUTE}


# Token validator for the authentication
@auth.verify_token
def verify_user_token(token):
    try:
        user_id = login_token_serializer.loads(token, max_age=SerializeConfig.LOGIN_TOKEN_AGE)
        return TeacherModel.query.get(user_id)
    except BadTimeSignature:
        abort(401, message=RestErrors.TOKEN_EXPIRED)
    except BadSignature:
        abort(401, message=RestErrors.INVALID_TOKEN)