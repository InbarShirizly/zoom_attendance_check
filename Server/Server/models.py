from Server import db, bcrypt, auth
from flask_login import UserMixin


@auth.verify_password
def get_user(username_or_email, password):
    user = TeacherModel.query.filter_by(email=username_or_email).first() or \
         TeacherModel.query.filter_by(username=username_or_email).first() # User can be validated with both username and email
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    

class TeacherModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # 60 chars because of the hashing algo
    classrooms = db.relationship('ClassroomModel', backref='teacher_model', lazy=True)
    
    def __repr__(self):
        return f'Teacher({self.username}, {self.email}, {self.password})'


class ClassroomModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher_model.id'), nullable=False)
    students = db.relationship('StudentModel', backref='classroom_model', lazy=True)
    reports = db.relationship('ReportModel', backref='classroom_model', lazy=True)


class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    id_number = db.Column(db.String(10), unique=False, nullable=True)
    org_class = db.Column(db.String(20), unique=False, nullable=True)
    gender = db.Column(db.Boolean, unique=False, nullable=True)  # True means male
    phone = db.Column(db.Integer, unique=False, nullable=True)

    class_id = db.Column(db.Integer, db.ForeignKey('classroom_model.id'), nullable=False)
    zoom_names = db.relationship('ZoomNamesModel', backref='student_model', lazy=True)


class ReportModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), unique=False, nullable=True)
    start_time = db.Column(db.DateTime(), unique=False, nullable=False) # first timestamp of chat file
    report_date = db.Column(db.Date(), unique=False, nullable=True) # date of the report - given by the user

    class_id = db.Column(db.Integer, db.ForeignKey('classroom_model.id'), nullable=False)
    sessions = db.relationship('SessionModel', backref='report_model', lazy=True)


class SessionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), unique=False, nullable=False) # first timestamp of chat session

    report_id = db.Column(db.Integer, db.ForeignKey('report_model.id'), nullable=False)
    zoom_names = db.relationship('ZoomNamesModel', backref='session_model', lazy=True)


class ZoomNamesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session_model.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student_model.id'), nullable=True) # if Null - means the student wasn't present in the session

    chat = db.relationship('ChatModel', backref='zoom_names_model', lazy=True)


class ChatModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=False, nullable=False)  # time the message written
    message = db.Column(db.Text, unique=False, nullable=True)  # message zoom user wrote
    relevant = db.Column(db.Boolean, unique=False, nullable=False)  # True is message is part of the report
    zoom_names_id = db.Column(db.Integer, db.ForeignKey('zoom_names_model.id'), nullable=False)



