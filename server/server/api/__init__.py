from flask_restful import Api
from flask import Blueprint

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)

from server.api import auth, clasrooms, reports, student_status
