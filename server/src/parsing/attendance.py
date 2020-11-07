import numpy as np
import pandas as pd
from src.parsing.session import Session
from src.parsing import AttendanceMetaData
from src.parsing.utils import clean_string

class Attendance:
    """
    receives student class df, the zoom chat and other configuration.
    returns:
     1. report_sessions - session object
     2. student_status_table - df of "student" table
    """
    def __init__(self, chat_df, students_df, filter_modes, time_delta, start_sentence, zoom_names_to_ignore):
        """
        :param chat_df: zoom chat (df)
        :param students_df: student class raw data (df)
        :param filter_modes: filters the user picked for parsing the text file (list of str)
        :param time_delta: max time from start sentence to the last message to parse in each session in minutes (int)
        :param start_sentence: start sentence that initiate sessions for parse (str)
        :param zoom_names_to_ignore: zoom names that will not be considered (list of str)
        :return: data frame with the data from the chat
        """
        # create a nametuple for several values
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence.lower(), zoom_names_to_ignore=zoom_names_to_ignore)

        self.first_message_time = chat_df["time"].sort_values().iloc[0] # get time of first message in the chat
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        self._df_students, report_df = Attendance.prepare_chat_and_classroom(students_df, chat_df)

        self._sessions = []
        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(report_df, start_indices, ind, time_delta)
            self._sessions.append(Session(self._df_students, df_session, meta_data))

    @staticmethod
    def prepare_chat_and_classroom(students_df, chat_df):
        # set all columns to str except the id
        df_students_for_report = students_df.set_index("id").astype(str)
        df_students_for_report = df_students_for_report.applymap(clean_string).reset_index()
        chat_df["message"] = chat_df["message"].apply(clean_string)
        return df_students_for_report, chat_df

    @staticmethod
    def get_start_indices(df, meta_data):
        """
        find start indices - when one of the "teachers" (zoom_names_to_ignore) writes the "start_sentence"
        :param df: zoom chat (df)
        :param meta_data: configurations of the user (namedtuple)
        :return: list of indices of start of session
        """
        not_included_zoom_users_filt = df['zoom_name'].str.contains('|'.join(meta_data.zoom_names_to_ignore))
        not_included_zoom_users_df = df[not_included_zoom_users_filt]
        check_sentence = lambda string: meta_data.start_sentence.lower() in string.lower()
        start_indices = not_included_zoom_users_df.index[not_included_zoom_users_df['message'].apply(check_sentence)]
        return start_indices

    @staticmethod
    def get_df_of_time_segment(df, start_indices, ind, time_delta):
        """
        slice the data-frame with the relevant chat - according to:
         1. last message in the time delta
         2. until next "start_index" (if there is next one)
        :param df: full chat df of the report (df)
        :param start_indices: list indices of start of session (list of int)
        :param ind: index of the current session
        :param time_delta: input time delta for last message in the session (int - minutes)
        :return: The relevant df of the session's chat (df)
        """
        if ind < len(start_indices) - 1:
            df = df.iloc[start_indices[ind]:start_indices[ind + 1], :]

        time_delta = np.timedelta64(time_delta, 'm')
        time_segment_start = df.loc[start_indices[ind], "time"]
        time_filt = (df["time"] >= time_segment_start) & \
                    (df["time"] <= time_segment_start + time_delta)

        relevant_df = df.loc[time_filt]
        return relevant_df

    @property
    def report_sessions(self):
        return self._sessions

    def student_status_table(self, report_id):
        """
        create the student statuses table that will be inserted to the database
        :param report_id: number of referring report in the DB
        :return: df of relevant data of student's statuses
        """
        df_status_report = self._df_students.loc[:, ["id", "name"]]
        for i, session_object in enumerate(self.report_sessions):
            # create columns for each session - if the student name id is part of the relevant chat (which means student wasn't missing) - row=1
            df_status_report[f"session_{i}"] = df_status_report["id"].apply(lambda x: 1 if x in session_object._relevant_chat["id"].values else np.nan)

        status = lambda row: 0 if row.isna().all() else (1 if row.isna().any() else 2)
        # check status of each student according to colors code {0 : "red", 1: "yellow", 2: "green"}
        df_status_report["status"] = df_status_report.loc[:, df_status_report.columns.str.startswith('session')].apply(status, axis=1)
        df_status_report['report_id'] = pd.Series([report_id] * df_status_report.shape[0])
        df_status_report.rename(columns={"id": "student_id"}, inplace=True)
        return df_status_report.loc[:, ["student_id", "report_id", "status"]]


