import numpy as np
import pandas as pd


class Attendance:
    """
    receives student class df, the zoom chat and other configuration.
    returns:
     1. report_sessions - session object
     2. student_status_table - df of "student" table
    """
    def __init__(self, chat_df, students_df, filter_modes, time_delta, start_sentence, not_included_zoom_users):
        """
        :param chat_df: zoom chat in df (df)
        :param students_df: student class raw data (df)
        :param filter_modes: filters the user picked for parsing the text file (list of str)
        :param time_delta: max time from start sentence to the last message to parse in each session in minutes (int)
        :param start_sentence: start sentence that initiate sessions for parse (str)
        :param not_included_zoom_users: zoom names that will not be considered (list of str)
        :return: data frame with the data from the chat
        """

        self.first_message_time = chat_df["time"].sort_values().iloc[0] # get time of first message in the chat
        start_indices = chat_df.index[chat_df['message'].apply(lambda string: start_sentence.lower() in string.lower())] #TODO: slice by time or by next message
        df_students_for_report = students_df.set_index("id").astype(str).reset_index()  # set all columns to str except the id
        self._df_students = df_students_for_report

        self._sessions = []
        for start_index in start_indices:
            df_session = Attendance.get_df_of_time_segment(chat_df, start_index, time_delta)
            self._sessions.append(Session(self._df_students, df_session, filter_modes, not_included_zoom_users))

    @staticmethod
    def get_df_of_time_segment(df, start_index, time_delta):
        
        time_delta = np.timedelta64(time_delta, 'm')
        time_segment_start = df.loc[start_index, "time"]
        time_filt = (df["time"] >= time_segment_start) & \
                    (df["time"] <= time_segment_start + time_delta)

        return df.loc[time_filt]

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


class Session:

    def __init__(self, students_df, df_session_chat, filter_modes, not_included_zoom_users):

        self._first_message_time = df_session_chat["time"].sort_values().iloc[0]
        self._relevant_chat = self.get_participants_in_session(students_df, filter_modes, df_session_chat, not_included_zoom_users)

    @ staticmethod
    def get_participants_in_session(df_students, filter_modes, df_chat, not_included_zoom_users):
        """
        finds students that attendant to the session. runs over each mode which represent different way to declare that
        the student attendant (for example: phone number, ID). merges this data to the csv table with the zoom name that
        added it
        :param df_chat: that table of the chat for the specific session
        :return: df of the attendance in the session
        """
        final_df = None
        for mode in filter_modes:
            merged_df = pd.merge(df_students, df_chat.reset_index(), left_on=mode, right_on="message", how="left")
            final_df = pd.concat([merged_df, final_df])

        final_df.sort_values(by="time", inplace=True)
        df_participated = final_df.groupby("zoom_name").first().reset_index()
        df_participated["index"] = df_participated["index"].astype(int)
        df_participated = df_participated.loc[:, ["id", "zoom_name", "time", "message", "index"]].set_index("index")

        filt = df_chat['zoom_name'].str.contains('|'.join(not_included_zoom_users))
        df_relevant_chat = pd.merge(df_chat[~filt], df_participated, how="left")

        df_relevant_chat["relevant"] = df_relevant_chat["id"].apply(lambda x: 1 if x == x else 0)
        df_relevant_chat["id"] = df_relevant_chat["id"].apply(lambda x: int(x) if x == x else -1)
        return df_relevant_chat


    def zoom_names_table(self, session_id):
        zoom_df = self._relevant_chat.loc[:, ["zoom_name", "id"]].rename(columns={"zoom_name": "name", "id": "student_id"})
        zoom_df['session_id'] = pd.Series([session_id] * zoom_df.shape[0])
        return zoom_df.sort_values(by="student_id", ascending=False).groupby("name").first().reset_index()

    def chat_table(self, zoom_df):
        relevant_chat = self._relevant_chat.drop(columns=["id"])
        chat_session_table = pd.merge(relevant_chat, zoom_df, left_on="zoom_name", right_on="name")
        return chat_session_table.drop(columns=["zoom_name", "name", "session_id", "student_id"]).rename(columns={"id": "zoom_names_id"})



if __name__ == '__main__':
    from utils import create_chat_df, create_students_df

    chat_file_path = r"C:\Users\Inbar Shirizly\Documents\python\useful\ITC_programs\zoom_attendance_check\chat files\meeting_example_full_name.txt"
    excel_file_path = r"C:\Users\Inbar Shirizly\Documents\python\useful\ITC_programs\zoom_attendance_check\student_csv_examples\example_data_already_prepared.xlsx"


    with open(chat_file_path, "r", encoding="utf-8") as f:
        chat_df = create_chat_df(f.readlines())
    df_students = create_students_df(file_name=excel_file_path.split("\\")[-1], file_data=excel_file_path)

    my_class = Attendance(chat_df, df_students, ['name', "id_number", "phone"], 5, "Attendance check", ["ITC", "Tech", "Challenge"])
    a = my_class.student_status_table(1)
    print(a)
    # df_part_session = my_class._sessions[0]
    # df_part_session.zoom_names_table(2)

