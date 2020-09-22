from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


class CreateClassForm(FlaskForm):
    name = StringField('Name of the class', validators=[DataRequired()])
    students_file = FileField('Csv/Excel file of students', validators=[FileAllowed(['xlsx', 'csv']), FileRequired()])
    submit = SubmitField('Create')
