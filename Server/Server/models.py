from Server import db, bcrypt, auth
from flask_login import UserMixin


@auth.verify_password
def get_user(username_or_email, password):
    user = TeacherModel.query.filter_by(email=username_or_email).first() or \
         TeacherModel.query.filter_by(username=username_or_email).first() # User can be validated with both username and email
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    

class TeacherModel(db.Model, UserMixin):
    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # 60 chars because of the hashing algo
   
    classrooms = db.relationship('ClassroomModel', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'Teacher({self.username}, {self.email}, {self.password})'


class ClassroomModel(db.Model):
    __tablename__ = 'classroom'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    students = db.relationship('StudentModel', backref='classroom', cascade="all,delete", lazy=True)
    reports = db.relationship('ReportModel', backref='classroom', cascade="all,delete", lazy=True)


class StudentModel(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    id_number = db.Column(db.String(10), unique=False, nullable=True)
    org_class = db.Column(db.String(20), unique=False, nullable=True)
    gender = db.Column(db.Boolean, unique=False, nullable=True)  # True means male
    phone = db.Column(db.Integer, unique=False, nullable=True)

    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    zoom_names = db.relationship('ZoomNamesModel', backref='student', lazy=True)
    statuses = db.relationship('StudentStatus', backref='student', lazy=True)


class ReportModel(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), unique=False, nullable=True)
    report_time = db.Column(db.DateTime(), unique=False, nullable=False) # first timestamp of chat file, date by user or date of the request

    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    sessions = db.relationship('SessionModel', backref='report',cascade="all,delete", lazy=True)
    student_statuses = db.relationship('StudentStatus', backref='report', cascade="all,delete", lazy=True)


class SessionModel(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), unique=False, nullable=False) # first timestamp of chat session

    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    zoom_names = db.relationship('ZoomNamesModel', backref='session',cascade="all,delete", lazy=True)


class ZoomNamesModel(db.Model):
    __tablename__ = 'zoom_names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)

    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True) # if Null - means the student wasn't present in the session
    chat = db.relationship('ChatModel', backref='zoom_name',cascade="all,delete", lazy=True)


class ChatModel(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=False, nullable=False)  # time the message written
    message = db.Column(db.Text, unique=False, nullable=True)  # message zoom user wrote
    relevant = db.Column(db.Boolean, unique=False, nullable=False)  # True is message is part of the report

    zoom_names_id = db.Column(db.Integer, db.ForeignKey('zoom_names.id'), nullable=False)


class StudentStatus(db.Model):
    __tablename__ = 'student_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, unique=False, nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

