from server.api import api
from flask_restful import Resource, reqparse, abort, marshal
from server.parsing.attendance import Attendance
from werkzeug.datastructures import FileStorage
from server import db, auth
from datetime import datetime
import pandas as pd
from server.models.orm import StudentModel, ClassroomModel, ReportModel, SessionModel, ZoomNamesModel, StudentStatus
from server.parsing.utils import create_chat_df
from server.api.utils import validate_classroom
from server.config import RestErrors
from server.models.marshals import student_status_field, reports_list_fields


class ReportsResource(Resource):
    method_decorators = [validate_classroom, auth.login_required]
    
    def __init__(self):
        super().__init__()
        self._post_args = reqparse.RequestParser()
        self._post_args.add_argument('description', type=str)
        self._post_args.add_argument('chat_file', type=FileStorage, help="Chat file is required", location='files', required=True)
        self._post_args.add_argument('time_delta', default=1, type=int)
        self._post_args.add_argument('date', default=datetime.now().date(), type=lambda x: datetime.strptime(x, '%d/%m/%y'))
        self._post_args.add_argument('first_sentence', type=str, help='First sentence is required in order to understand when does the check starts', required=True)
        self._post_args.add_argument('not_included_zoom_users', default=[], type=str, help='Must be a list of strings with zoom names', action="append")

    def get(self, class_id, report_id=None):
        if report_id is None:
            return marshal(ReportModel.query.filter_by(class_id=class_id).all(), reports_list_fields)
        report = ReportModel.query.filter_by(class_id=class_id, id=report_id).first()
        if report is None:
            abort(400, message=RestErrors.INVALID_REPORT)
        return marshal(report.student_statuses, student_status_field)
        
    def post(self, class_id, report_id=None):
        if report_id:
            abort(404, message=RestErrors.INVALID_REPORT)
        args = self._post_args.parse_args()

        students_df = pd.read_sql(StudentModel.query.filter_by(class_id=class_id).statement, con=db.engine)


        chat_file = args['chat_file'].stream.read().decode("utf-8").split("\n") #TODO: check this in test
        chat_df = create_chat_df(chat_file)
        report_object = Attendance(chat_df, students_df, ['name', "id_number", "phone"], args['time_delta'], args['first_sentence'], args['not_included_zoom_users'])

        message_time = report_object.first_message_time
        report_time = datetime(args["date"].year, args["date"].month, args["date"].day,
                               message_time.hour, message_time.minute, message_time.second)

        new_report = ReportModel(description=args['description'], report_time=report_time, class_id=class_id)
        db.session.add(new_report)
        db.session.commit()

        student_status_df = report_object.student_status_table(new_report.id)
        student_status_df.to_sql('student_status', con=db.engine, if_exists="append", index=False)

        for session_object in report_object.report_sessions:
            session_table = SessionModel(start_time=session_object._first_message_time, report_id=new_report.id)
            db.session.add(session_table)
            db.session.commit()

            zoom_names_df = session_object.zoom_names_table(session_table.id)
            zoom_names_df.to_sql('zoom_names', con=db.engine, if_exists="append", index=False)

            zoom_names_df = pd.read_sql(ZoomNamesModel.query.filter_by(session_id=session_table.id).statement, con=db.engine)
            session_chat_df = session_object.chat_table(zoom_names_df)
            session_chat_df.to_sql('chat', con=db.engine, if_exists="append", index=False)

        return {"report_id": new_report.id}

    def delete(self, class_id, report_id=None):
        if report_id is None:  # Deleting all reports of class
            class_reports_id = db.session.query(ReportModel.id).filter_by(class_id=class_id).all()
            for report_data in class_reports_id:
                current_report = ReportModel.query.filter_by(id=report_data.id).first()
                db.session.delete(current_report)
            db.session.commit()
            return "", 204

        current_report = ReportModel.query.filter_by(id=report_id).first()  # Making sure the class belongs to the current user
        if current_report is None:
            abort(400, message=RestErrors.INVALID_REPORT)

        db.session.delete(current_report)
        db.session.commit()
        return "", 204

api.add_resource(ReportsResource, '/classrooms/<int:class_id>/reports', '/classrooms/<int:class_id>/reports/<int:report_id>')
