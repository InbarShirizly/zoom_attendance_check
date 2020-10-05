from flask_restful import Api
from flask import Blueprint
from server.api.validators import Validators
from server.config import ValidatorsConfig

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
custom_types = Validators.from_object(ValidatorsConfig)

from server.api import auth, clasrooms, reports, student_status
