from flask_restful import Api
from flask import Blueprint
from src.api.validators import Validators
from src.config import ValidatorsConfig, FlaskConfig, SerializeConfig
from itsdangerous import URLSafeTimedSerializer

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
custom_types = Validators.from_object(ValidatorsConfig)
login_token_serializer = URLSafeTimedSerializer(FlaskConfig.SECRET_KEY, salt=SerializeConfig.LOGIN_SALT)

from src.api import auth, clasrooms, reports, student_status, student
