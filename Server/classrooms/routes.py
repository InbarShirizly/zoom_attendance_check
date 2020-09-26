from flask import render_template, redirect, url_for, flash, Blueprint, request, session
from Server import db
from Server.classrooms.forms import CreateClassForm, CreateReportForm
from Server.models import Classroom, Student
from flask_login import current_user, login_required
import pandas as pd
from Server.classrooms.attendance_check import Attendance
from Server.classrooms.utils import create_chat_df, create_students_df
from Server.classrooms import parser

classrooms = Blueprint('classrooms', __name__)


@classrooms.route('/', methods=['GET', 'POST'])
@classrooms.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CreateClassForm()
    if form.validate_on_submit():
        students_df = create_students_df(form.students_file.data.filename, form.students_file.data)
        students = parser.parse_df(students_df)
        new_class = Classroom(name=form.name.data, teacher=current_user)
        db.session.add(new_class)
        db.session.commit()
        students['class_id'] = pd.Series([new_class.id] * students.shape[0])
        students.to_sql('student', con=db.engine, if_exists="append", index=False)
        return redirect(url_for('classrooms.classroom', class_id=new_class.id))
    return render_template('home.html', form=form)


@classrooms.route('/classroom/<class_id>', methods=['GET', 'POST'])
@login_required
def classroom(class_id):
    current_class = Classroom.query.filter_by(id=class_id, teacher=current_user).first() # Making sure the class belongs to the current user
    if current_class is None:
        flash('Invalid class!', 'danger')
        return redirect(url_for('classrooms.home'))
    
    form = CreateReportForm() 
    if form.validate_on_submit(): # If form was submitted, creating report for the class
        students_df = pd.read_sql(Student.query.filter_by(class_id=class_id).statement, con=db.engine)
        chat_df = create_chat_df(form.chat_file.data.stream)

        my_class = Attendance(chat_df, students_df, ['name', "id_number", "phone"], form.time.data, form.start_sentence.data)
        attendance_df, df_zoom_not_correct_list = my_class.get_attendance(["ITC", "Tech", "Challenge"])
        return render_template("report.html")
        

    return render_template('classroom.html', current_class=current_class, form=form)


