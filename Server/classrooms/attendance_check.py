"""
----------- zoom check attendance -----------
Program implementations:
a. gets a text file - zoom chat from class
b. find session when an attendance check has been initiated and look for all the participators who wrote
    something meaningful in the chat before or after the check. function checks allows user to write a name of the
    student list only once. in case user had a mistake, it will check all his messages until it find the relevant one
c. return df contains all the users from the csv/excel file with new columns that have: zoom name/ Nan - where zoom name
    means that this zoom user added the relevant name and Nan means missing student
d. retrun df from each session with the messages of zoom users that did not write something related to the actuall name
    (allows the teacher to check if they had type error and then add them manually)

"""

from datetime import datetime
import numpy as np
import pandas as pd
import re
import conf

# configuration variables
FILE_NAME = ".\chat files\meeting_example_full_name.txt"
EXCEL_PATH = "דוגמה לרשימת תלמידים.xlsx"
SENTENCE_START = "attendance check"
TIME_DELTA = 1  # time period in minuets
WORDS_FOR_NOT_INCLUDED_PARTICIPATORS = ["ITC", "Tech", "Challenge"]


class Attendance:

    def __init__(self, chat_path, student_file_path, filter_modes, time_delta, start_sentence):
        """
        - convert the chat text file to a data frame and arrange columns.
        - creates df for each session according the appearance of the start sentence and time delta
        - create df from the excel or csv file of the studnets
        :param chat_path: the path of the relevant chat file (str)
        :param student_file_path: path for the relevant csv/excel file (str)
        :param filter_modes: filters the user picked for parsing the text file (list of str)
        :param time_delta: max time from start sentence to the last message to parse in each session in minutes (int)
        :param start_sentence: start sentence that initiate sessions for parse (str)
        :return: data frame with the data from the chat
        """
        with open(chat_path, "r", encoding="utf-8") as file:
            data = [re.search(conf.CHAT_PATTERN, line).groups() for line in file if re.match(conf.CHAT_PATTERN, line)]
        df = pd.DataFrame(data, columns=["time", "users", "chat"])
        df['chat'] = df['chat'].str[:-1]
        df["time"] = df["time"].apply(lambda string: datetime.strptime(string, "%H:%M:%S"))

        start_indices = df.index[df['chat'].apply(lambda string: start_sentence.lower() in string.lower())]

        self.df_sessions = [self.get_df_of_time_segment(df, start_index, time_delta) for start_index in start_indices]
        self.filter_modes = filter_modes
        if student_file_path.endswith(".csv"):
            self.df_students = pd.read_csv(student_file_path, usecols=conf.EXCEL_COLS.values()).astype("str")
        else:
            self.df_students = pd.read_excel(student_file_path, usecols=conf.EXCEL_COLS.values()).astype("str")

    @staticmethod
    def get_df_of_time_segment(df, start_index, time_delta):
        
        time_delta = np.timedelta64(time_delta, 'm')
        time_segment_start = df.loc[start_index, "time"]
        time_filt = (df["time"] >= time_segment_start) & \
                    (df["time"] <= time_segment_start + time_delta)

        return df.loc[time_filt]


    def get_participants(self, df_chat):
        """
        finds students that attendant to the session. runs over each mode which represent different way to declare that
        the student attendant (for example: phone number, ID). merges this data to the csv table with the zoom name that
        added it
        :param df_chat: that table of the chat for the specific session
        :return: df of the attendance in the session
        """
        final_df = None
        for mode in self.filter_modes:
            merged_df = pd.merge(self.df_students, df_chat, left_on=conf.EXCEL_COLS[mode], right_on="chat", how="left")
            final_df = pd.concat([merged_df, final_df])

        final_df.sort_values(by="time", inplace=True)
        df_participated = final_df.drop(columns=["chat", "time"])
        df_participated = df_participated.groupby("users").first().reset_index()

        df_participated_updated = pd.merge(self.df_students, df_participated, left_on=conf.EXCEL_COLS["Name"],
                                           right_on=conf.EXCEL_COLS["Name"], how="left", suffixes=["_x", ""])
        overlapping_columns = df_participated_updated.columns[df_participated_updated.columns.str.contains("_x")]
        df_participated_updated = df_participated_updated.drop(columns=overlapping_columns)
        return df_participated_updated

    @staticmethod
    def get_zoom_users_not_included(df_participated, df_chat, not_included_part):
        """
        get the zoom users who wrote something in the chat but it was not related to the csv/excel users info
        - drops not relevant records from the df of zoom users that are not part of the class
        - drops the zoom users who wrote something meaningful
        :param df_participated: output of participators - that contains Nan for csv student that weren't mentioned (df)
        :param df_chat: full chat of the relevant session (df)
        :param not_included_part: zoom user name that will not be included (list of str)
        :return: table of zoom users and there messages in the session (df)
        """
        filt = ~(df_chat['users'].isin(df_participated['users'].dropna())) & \
               ~(df_chat['users'].str.contains('|'.join(not_included_part)))
        df_zoom_not_correct = df_chat[filt]
        return df_zoom_not_correct.drop(columns=["time"]).set_index("users")

    def get_attendance(self, not_included_part):
        """
        - get table of attendant student from the csv/excel file and list of table of relevant data from zoom users that
          didn't add a student.
        - runs over all the session, for each one take the zoom user names and add it as a column to the final df -
          if there is Nan it means that the student was missing in that session. the zoom user name is the user who added
          the specific student.
        - for each session append to a list all the df represent table of relevant data from zoom users that
          didn't add a student
        :param not_included_part: zoom user name that will not be included (list of str) 
        :return: 1. table of attendant student from the csv/excel file,
                 2. list of table of relevant data from zoom users that didn't add a student
        """
        df_zoom_not_correct_list = []
        attendance_df = self.df_students
        for i, session in enumerate(self.df_sessions):
            df_participated = self.get_participants(session)
            attendance_df[f'session {i + 1}'] = df_participated['users']
            df_zoom_not_correct = self.get_zoom_users_not_included(df_participated, session, not_included_part)
            df_zoom_not_correct_list.append(df_zoom_not_correct)

        return attendance_df, df_zoom_not_correct_list

def main():
    my_class = Attendance(FILE_NAME, EXCEL_PATH, ['Name', "ID", "Phone"], TIME_DELTA, SENTENCE_START)
    attendance_df, df_zoom_not_correct_list = my_class.get_attendance(WORDS_FOR_NOT_INCLUDED_PARTICIPATORS)

    print(attendance_df)

    for i in range(len(df_zoom_not_correct_list)):
        print(f"zoom session {i + 1}")
        print(df_zoom_not_correct_list[i])


if __name__ == '__main__':
     main()

