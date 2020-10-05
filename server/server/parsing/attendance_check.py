import numpy as np
import pandas as pd
from server.parsing.session import Session
from server.parsing import AttendanceMetaData


class Attendance:
    """
    receives student class df, the zoom chat and other configuration.
    returns:
     1. report_sessions - session object
     2. student_status_table - df of "student" table
    """
    def __init__(self, chat_df, students_df, filter_modes, time_delta, start_sentence, not_included_zoom_users):
        """
        :param chat_df: zoom chat (df)
        :param students_df: student class raw data (df)
        :param filter_modes: filters the user picked for parsing the text file (list of str)
        :param time_delta: max time from start sentence to the last message to parse in each session in minutes (int)
        :param start_sentence: start sentence that initiate sessions for parse (str)
        :param not_included_zoom_users: zoom names that will not be considered (list of str)
        :return: data frame with the data from the chat
        """
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, not_included_zoom_users=not_included_zoom_users)

        self.first_message_time = chat_df["time"].sort_values().iloc[0] # get time of first message in the chat
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        df_students_for_report = students_df.set_index("id").astype(str).reset_index()  # set all columns to str except the id
        self._df_students = df_students_for_report

        self._sessions = []
        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(chat_df, start_indices, ind, time_delta)
            self._sessions.append(Session(self._df_students, df_session, meta_data))

    @staticmethod
    def get_start_indices(df, meta_data):
        """
        find start indices - when one of the "teachers" writes the "start_sentence"
        :param df: zoom chat (df)
        :param meta_data: configurations of the user
        :return: list of indices of start of session
        """
        not_included_zoom_users_filt = df['zoom_name'].str.contains('|'.join(meta_data.not_included_zoom_users))
        not_included_zoom_users_df = df[not_included_zoom_users_filt]
        check_sentence = lambda string: meta_data.start_sentence.lower() in string.lower()
        start_indices = not_included_zoom_users_df.index[not_included_zoom_users_df['message'].apply(check_sentence)]
        return start_indices


    @staticmethod
    def get_df_of_time_segment(df, start_indices, ind, time_delta):
        """

        :param df:
        :param start_indices:
        :param ind:
        :param time_delta:
        :return:
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
        df_status_report = self._df_students.loc[:, ["id", "name"]]
        for i, session_object in enumerate(self.report_sessions):
            df_status_report[f"session_{i}"] = df_status_report["id"].apply(lambda x: 1 if x in session_object._relevant_chat["id"].values else np.nan)

        status = lambda row: 0 if row.isna().all() else (1 if row.isna().any() else 2)  # {0 : "red", 1: "yellow", 2: "green"}
        df_status_report["status"] = df_status_report.loc[:, df_status_report.columns.str.startswith('session')].apply(status, axis=1)
        df_status_report['report_id'] = pd.Series([report_id] * df_status_report.shape[0])
        df_status_report.rename(columns={"id": "student_id"}, inplace=True)
        return df_status_report.loc[:, ["student_id", "report_id", "status"]]


if __name__ == '__main__':
    from collections import namedtuple
    from utils import create_chat_df, create_students_df

    AttendanceMetaData = namedtuple('meta_data',
                                    ['filter_modes', 'time_delta', 'start_sentence', 'not_included_zoom_users'])

    chat_file_path = r"C:\Users\Inbar Shirizly\Documents\python\useful\ITC_programs\zoom_attendance_check\chat files\meeting_example_full_name.txt"
    excel_file_path = r"C:\Users\Inbar Shirizly\Documents\python\useful\ITC_programs\zoom_attendance_check\student_csv_examples\example_data_already_prepared.xlsx"


    with open(chat_file_path, "r", encoding="utf-8") as f:
        chat_df = create_chat_df(f.readlines())
    df_students = create_students_df(file_name=excel_file_path.split("\\")[-1], file_data=excel_file_path)

    my_class = Attendance(chat_df, df_students, ['name', "id_number", "phone"], 1, "Attendance check", ["ITC", "Tech", "Challenge"])
    a = my_class.student_status_table(1)
    print(a)
    # df_part_session = my_class._sessions[0]
    # df_part_session.zoom_names_table(2)

