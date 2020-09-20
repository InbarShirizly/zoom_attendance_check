from Server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # 60 chars because of the hashing algo
    classes = db.relationship('Classroom', backref='teacher', lazy=True)


class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    csv_students_file = db.Column(db.String(120), unique=True, nullable=False)
    # TODO: also store the reports in the db