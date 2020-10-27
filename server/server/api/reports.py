from server.api import api, custom_types
from flask_restful import Resource, reqparse, abort, marshal, marshal_with
from server.parsing.attendance import Attendance
from server import db, auth
from datetime import datetime
import pandas as pd
from server.models.orm import StudentModel, ClassroomModel, ReportModel, SessionModel, ZoomNamesModel, StudentStatus
from server.api.utils import validate_classroom
from server.config import RestErrors, ValidatorsConfig
from server.models.marshals import report_resource_field, reports_list_fields
from server.models.utils import store_sessions_and_chat_data
from server.config import FlaskConfig

class ReportsResource(Resource):
    """
    Resource responsible for report handling (creating new report, getting report information, deleting report)
    """
    method_decorators = [validate_classroom, auth.login_required]
    
    def __init__(self):
        super().__init__()
        self._post_args = reqparse.RequestParser(bundle_errors=True)
        self._post_args.add_argument('description', type=str)
        self._post_args.add_argument('chat_file', type=custom_types.chat_file, location='files', required=True)
        self._post_args.add_argument('time_delta', help=RestErrors.INVALID_TIME_DELTA, type=int, required=True) # TODO: limit time up to 15 minutes
        self._post_args.add_argument('date', default=datetime.now(), type=custom_types.date)
        self._post_args.add_argument('first_sentence', type=str, required=True)
        self._post_args.add_argument('not_included_zoom_users', default=[], type=str, action="append")

    def get(self, class_id, report_id=None):
        """
        get information about all the reports of the given classroom or for a specific report if given
         - info returned from reports_list_fields (in marshals module)
        :param class_id: id of class to present (int)
        :param report_id: id of report to present - if not passed will return all reports (int)
        :return: report/s data (json)
        """
        if report_id is None:
            return marshal(ReportModel.query.filter_by(class_id=class_id).all(), reports_list_fields)
        report = ReportModel.query.filter_by(class_id=class_id, id=report_id).first()
        if report is None:
            abort(400, message=RestErrors.INVALID_REPORT)
        return marshal(report, report_resource_field)
    
    @marshal_with(report_resource_field)
    def post(self, class_id, report_id=None):
        """
        create a new report for the class given from the url.
        - info returned from report_resource_field (in marshals module)
        :param class_id: id of classroom related to the report
        :param report_id: should not be passed (we are creating new report - exist because of the resource format)
        :params - more params passing from the RequestParser of the user - including the chat and other configurations
                - more info about these in the init of in the api-doc
        :return: the new report data (json)
        """
        if report_id:
            abort(404, message=RestErrors.INVALID_REPORT)

        # If the classroom has more reports then max allowed - will aboort
        if len(ReportModel.query.filter_by(class_id=class_id).all()) >= ValidatorsConfig.MAX_REPORTS:
            abort(400, message=RestErrors.MAX_REPORTS)

        args = self._post_args.parse_args()

        students_df = pd.read_sql(StudentModel.query.filter_by(class_id=class_id).statement, con=db.engine)
        report_object = Attendance(args['chat_file'], students_df,
                                   ['name', "id_number", "phone", "country", "country_code"],
                                   args['time_delta'], args['first_sentence'],
                                   args['not_included_zoom_users'])  #TODO: should get "filters" from config

        new_report = ReportModel(description=args['description'], report_time=args["date"], class_id=class_id)
        db.session.add(new_report)
        db.session.commit()

        student_status_df = report_object.student_status_table(new_report.id)
        student_status_df.to_sql('student_status', con=db.engine, if_exists="append", index=False)

        # checks if to store the data for the session, chat and zoom names in the report
        if FlaskConfig.STORE_CHAT:
            # store all the chat, session and zoom names data from a report -  currently not supported
            store_sessions_and_chat_data(report_object.report_sessions, new_report.id)

        return new_report

    def delete(self, class_id, report_id=None):
        """
        delete a specific report from the class or all the reports. deleting a report will delete all the related tables
        under it: "zoom names", "session", "chat", "student_status"
        :param class_id: id of classroom to delete from
        :param report_id: id of report to delete - if "None" will delete all the reports of the class
        :return: 204 http code if succeeded
        """
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
