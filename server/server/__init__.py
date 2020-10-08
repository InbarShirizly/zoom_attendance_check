from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from server.config import FlaskConfig
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(FlaskConfig)
CORS(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
auth = HTTPTokenAuth("Bearer")


from server.api import api_blueprint

app.register_blueprint(api_blueprint)

