from flask import render_template, redirect, url_for, flash, Blueprint
from Server import db
from Server.classrooms.forms import CreateClassForm
from Server.models import Classroom, Student
from flask_login import current_user, login_required
from Server.classrooms.utils import save_file

classrooms = Blueprint('classrooms', __name__)


@classrooms.route('/', methods=['GET', 'POST'])
@classrooms.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CreateClassForm()
    if form.validate_on_submit():
        file_name = save_file(form.students_file.data)
        new_class = Classroom(name=form.name.data, teacher=current_user)
        db.session.add(new_class)
        db.session.commit()
    return render_template('home.html', form=form)


@classrooms.route('/classroom/<class_id>')
@login_required
def classroom(class_id):
    current_class = Classroom.query.filter_by(id=class_id, teacher=current_user).first() # Making sure the class belongs to the current user
    if current_class is None:
        flash('Invalid class!', 'danger')
        return redirect(url_for('classrooms.home'))
    current_class.students = [ # Temporary hardocded data
        Student(school_class='יב 1', name='איתי'), 
        Student(school_class='יב 2', name='ענבר', id_number=212525489),
        Student(school_class='יב 3', name='לירן', id_number=3),
        Student(school_class='Liran', name='hello')
    ]
    return render_template('classroom.html', current_class=current_class)

