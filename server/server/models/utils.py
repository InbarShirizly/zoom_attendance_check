from server import auth, bcrypt
from server.models.orm import TeacherModel

def get_user(username_or_email, password):
    user = TeacherModel.query.filter_by(email=username_or_email).first() or \
         TeacherModel.query.filter_by(username=username_or_email).first() # User can be validated with both username and email
    if user and bcrypt.check_password_hash(user.password, password):
        return user


    