from Server import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(int(user_id))


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # 60 chars because of the hashing algo
    classrooms = db.relationship('Classroom', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'Teacher({self.username}, {self.email}, {self.password})'


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    students = db.relationship('Student', backref='classroom', lazy=True)
    reports = db.relationship('Report', backref='classroom', lazy=True)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=False, nullable=False)
    id_number = db.Column(db.String(10), unique=False, nullable=True)
    org_class = db.Column(db.String(20), unique=False, nullable=True)
    gender = db.Column(db.Boolean, unique=False, nullable=True)  # True means male
    phone = db.Column(db.Integer, unique=False, nullable=True)

    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    student_in_session = db.relationship('StudentInSession', backref='student', lazy=True)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), unique=False, nullable=True)
    start_time = db.Column(db.DateTime(), unique=False, nullable=False) # first timestamp of chat file
    report_date = db.Column(db.Date(), unique=False, nullable=True) # date of the report - given by the user

    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    sessions = db.relationship('Session', backref='report', lazy=True)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), unique=False, nullable=False) # first timestamp of chat session

    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    student_in_session = db.relationship('StudentInSession', backref='session', lazy=True)


class ZoomNames(db.Model):
    __tablename__ = 'zoom_names'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)

    chat = db.relationship('Chat', backref='zoom_names', lazy=True)
    student_in_session = db.relationship('StudentInSession', backref='zoom_names', lazy=True)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, unique=False, nullable=False)  # time the message written
    message = db.Column(db.Text, unique=False, nullable=True)  # message zoom user wrote
    relevant = db.Column(db.Boolean, unique=False, nullable=False)  # True is message is part of the report
    zoom_names_id = db.Column(db.Integer, db.ForeignKey('zoom_names.id'), nullable=False)


class StudentInSession(db.Model):
    __tablename__ = 'student_in_session'
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    zoom_names_id = db.Column(db.Integer, db.ForeignKey('zoom_names.id'), nullable=False)



