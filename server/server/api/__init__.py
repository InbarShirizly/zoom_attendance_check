from flask_restful import Api
from flask import Blueprint
from server.api.validators import Validators
from server.config import ValidatorsConfig

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
custom_types = Validators(ValidatorsConfig.INVALID_USERNAME_CHARS, ValidatorsConfig.MIN_PASSWORD_LEN, ValidatorsConfig.REQUIRED_PASSWORD_CHARS)

from server.api import auth, clasrooms, reports, student_status
