from server import auth, bcrypt, db
from server.models.orm import TeacherModel, SessionModel,ZoomNamesModel
import pandas as pd

def get_user(username_or_email, password):
    user = TeacherModel.query.filter_by(email=username_or_email).first() or \
         TeacherModel.query.filter_by(username=username_or_email).first() # User can be validated with both username and email
    if user and bcrypt.check_password_hash(user.password, password):
        return user


def store_sessions_and_chat_data(report_sessions, report_id):  # store sessions and chat data for a specific report

    for session_object in report_sessions:
        session_table = SessionModel(start_time=session_object._first_message_time, report_id=report_id)
        db.session.add(session_table)
        db.session.commit()

        zoom_names_df = session_object.zoom_names_table(session_table.id)
        zoom_names_df.to_sql('zoom_names', con=db.engine, if_exists="append", index=False)

        zoom_names_df = pd.read_sql(ZoomNamesModel.query.filter_by(session_id=session_table.id).statement,
                                    con=db.engine)
        session_chat_df = session_object.chat_table(zoom_names_df)
        session_chat_df.to_sql('chat', con=db.engine, if_exists="append", index=False)



    