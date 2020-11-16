from flask_restful import Api
from flask import Blueprint
from app.api.validators import Validators
from app.config import ValidatorsConfig, FlaskConfig, SerializeConfig
from itsdangerous import URLSafeTimedSerializer

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
custom_types = Validators.from_object(ValidatorsConfig)
login_token_serializer = URLSafeTimedSerializer(FlaskConfig.SECRET_KEY, salt=SerializeConfig.LOGIN_SALT)

from app.api import auth, clasrooms, reports, student_status, student
