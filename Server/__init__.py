from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from Server.config import FlaskConfig

app = Flask(__name__)
app.config.from_object(FlaskConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from Server.users.routes import users
from Server.classrooms.routes import classrooms

app.register_blueprint(users)
app.register_blueprint(classrooms)

