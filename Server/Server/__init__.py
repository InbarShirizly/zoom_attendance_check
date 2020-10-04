from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from server.config import FlaskConfig
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(FlaskConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth(app)


from server.api import api_blueprint

app.register_blueprint(api_blueprint)

