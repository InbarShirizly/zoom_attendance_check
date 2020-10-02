from flask import render_template, redirect, url_for, flash, Blueprint, request, session
from Server import db
from Server.classrooms.forms import CreateClassForm, CreateReportForm
from Server.models import ClassroomModel, StudentModel, ReportModel, SessionModel, ZoomNamesModel, ChatModel
from flask_login import current_user, login_required
import pandas as pd
from Server.classrooms.attendance_check import Attendance
from Server.classrooms.utils import create_chat_df, create_students_df
from Server.classrooms import parser
from  datetime import datetime

classrooms = Blueprint('classrooms', __name__)


@classrooms.route('/', methods=['GET', 'POST'])
@classrooms.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CreateClassForm()
    if form.validate_on_submit():
        students_df = create_students_df(form.students_file.data.filename, form.students_file.data)
        students = parser.parse_df(students_df)
        new_class = ClassroomModel(name=form.name.data, teacher_model=current_user)
        db.session.add(new_class)
        db.session.commit()
        students['class_id'] = pd.Series([new_class.id] * students.shape[0])
        students.to_sql('student_model', con=db.engine, if_exists="append", index=False)
        return redirect(url_for('classrooms.classroom', class_id=new_class.id))
    return render_template('home.html', form=form)


@classrooms.route('/classroom/<class_id>', methods=['GET', 'POST'])
@login_required
def classroom(class_id):
    current_class = ClassroomModel.query.filter_by(id=class_id, teacher_model=current_user).first() # Making sure the class belongs to the current user
    if current_class is None:
        flash('Invalid class!', 'danger')
        return redirect(url_for('classrooms.home'))
    
    form = CreateReportForm() 
    if form.validate_on_submit(): # If form was submitted, creating report for the class
        description = "this is the best class"  # TODO : add from the form file
        report_date = datetime.now().date()    # TODO : add from the form file
        students_df = pd.read_sql(StudentModel.query.filter_by(class_id=class_id).statement, con=db.engine)
        chat_file = form.chat_file.data.stream.read().decode("utf-8").split("\n")
        chat_df = create_chat_df(chat_file)

        report_object = Attendance(chat_df, students_df, ['name', "id_number", "phone"], form.time.data, form.start_sentence.data, ["ITC", "Tech", "Challenge"])

        new_report = ReportModel(description=description, start_time=report_object.first_message_time, report_date=report_date, class_id=class_id)
        db.session.add(new_report)
        db.session.commit()

        # insert relevant data for each session to the database
        for session_object in report_object.report_sessions:
            session_table = SessionModel(start_time=session_object._first_message_time, report_id=new_report.id)
            db.session.add(session_table)
            db.session.commit()

            zoom_names_df = session_object.zoom_names_table(session_table.id)
            zoom_names_df.to_sql('zoom_names_model', con=db.engine, if_exists="append", index=False)

            zoom_names_df = pd.read_sql(ZoomNamesModel.query.filter_by(session_id=session_table.id).statement, con=db.engine)
            session_chat_df = session_object.chat_table(zoom_names_df)
            session_chat_df.to_sql('chat_model', con=db.engine, if_exists="append", index=False)



        return render_template("report.html")
        

    return render_template('classroom.html', current_class=current_class, form=form)


