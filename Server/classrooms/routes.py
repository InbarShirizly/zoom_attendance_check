from flask import render_template, redirect, url_for, flash, Blueprint, request
from Server import db
from Server.classrooms.forms import CreateClassForm, CreateReportForm
from Server.models import Classroom, Student
from flask_login import current_user, login_required
from Server.classrooms.loading_classroom_file import parse_excel
import pandas as pd

classrooms = Blueprint('classrooms', __name__)


@classrooms.route('/', methods=['GET', 'POST'])
@classrooms.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CreateClassForm()
    if form.validate_on_submit():
        students = parse_excel(form.students_file.data.filename, form.students_file.data)
        new_class = Classroom(name=form.name.data, teacher=current_user)
        db.session.add(new_class)
        db.session.commit()
        students['class_id'] = pd.Series([new_class.id] * students.shape[0])
        students.to_sql('student', con=db.engine, if_exists="append", index=False)


        # return redirect(url_for('classrooms.classroom', class_id=new_class.id))
    return render_template('home.html', form=form)


@classrooms.route('/classroom/<class_id>')
@login_required
def classroom(class_id):
    current_class = Classroom.query.filter_by(id=class_id, teacher=current_user).first() # Making sure the class belongs to the current user
    if current_class is None:
        flash('Invalid class!', 'danger')
        return redirect(url_for('classrooms.home'))
    form = CreateReportForm()
    return render_template('classroom.html', current_class=current_class, form=form)
