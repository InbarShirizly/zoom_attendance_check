from flask_restful import Api
from flask import Blueprint
from server.api.validators import Validators
from server.config import ValidatorsConfig, FlaskConfig
from itsdangerous import URLSafeSerializer

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
custom_types = Validators.from_object(ValidatorsConfig)
login_token_serializer = URLSafeSerializer(FlaskConfig.SECRET_KEY, salt="login")

from server.api import auth, clasrooms, reports, student_status
