"""
----------- zoom check attendance -----------
Program implementations:
a. gets a text file - zoom chat from class
b. find when an attendance check has been initiated and look for all the participators who wrote
something in the chat before or after the check
c. finds the connection between the zoom name and the student full name (Could be from a cache of these connections
in a json file, after getting all the connections, update the json file with all the new occurrences (if were some)
d. prints all the missing students by subtracting the participators from the total students in class
e. this program can run over multiple attendance check in the same file

a config file is attached to this program with all the related variables
"""

from datetime import datetime
import numpy as np
import pandas as pd
import re
import conf


class attendance:

    def __init__(self, chat_path, filter_modes):
        """
        convert the chat text file to a data frame.
        change time to date and remove "\n" from the chat
        :param chat_path: the path of the relevant chat file (str)
        :return: data frame with the data from the chat
        """
        with open(chat_path, "r", encoding="utf-8") as file:
            data = [re.search(conf.CHAT_PATTERN, line).groups() for line in file if re.match(conf.CHAT_PATTERN, line)]
        df = pd.DataFrame(data, columns=conf.COLUMNS_NAMES)
        df['chat'] = df['chat'].str[:-1]
        df["time"] = df["time"].apply(lambda string: datetime.strptime(string, "%H:%M:%S"))

        self.full_chat_df = df
        start_indices = df.index[df['chat'].apply(lambda string: conf.SENTENCE_START.lower() in string.lower())]
        self.time_delta = np.timedelta64(conf.TIME_DELTA, 'm')
        self.df_sessions = [self.get_df_of_time_segment(start_index) for start_index in start_indices]
        self.filter_modes = filter_modes
        self.df_students = pd.read_excel(conf.EXCEL_PATH, usecols=conf.EXCEL_COLS.values()).astype("str")
        self.attendance_df = self.df_students

    def get_df_of_time_segment(self, start_index):
        time_segment_start = self.full_chat_df.loc[start_index, "time"]
        time_filt = (self.full_chat_df["time"] >= time_segment_start) & \
                    (self.full_chat_df["time"] <= time_segment_start + self.time_delta)

        return self.full_chat_df.loc[time_filt]


    def get_participants(self, df_chat):
        """
        parse the data frame of the chat data to find the participants in the meeting that
        wrote something in a period of time after a specific sentence had been writen
        zoom user with name that will be probably the lecturer is deleted
        :param df_chat: data frame of the chat content
        :param start_index: start index of session
        :return: participants in the zoom meeting (exclude lecturer) - (list_
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
    def get_zoom_users_not_included(df_participated, df_chat):
        filt = ~(df_chat['users'].isin(df_participated['users'].dropna())) & \
               ~(df_chat['users'].str.contains('|'.join(conf.WORDS_FOR_NOT_INCLUDED_PARTICIPATORS)))
        df_zoom_not_correct = df_chat[filt]
        return df_zoom_not_correct.drop(columns=["time"]).set_index("users")

    def get_attendance(self):
        df_zoom_not_correct_list  = []
        for i in range(len(self.df_sessions)):

            df_participated = self.get_participants(self.df_sessions[i])
            self.attendance_df[f'session {i + 1}'] = df_participated['users']
            df_zoom_not_correct = self.get_zoom_users_not_included(df_participated, self.df_sessions[i])
            df_zoom_not_correct_list.append(df_zoom_not_correct)

        return self.attendance_df, df_zoom_not_correct_list

def main():
    my_class = attendance(conf.FILE_NAME, ['Name', "ID", "Phone"])

    attendance_df, df_zoom_not_correct_list = my_class.get_attendance()

    print(attendance_df)

    for i in range(len(df_zoom_not_correct_list)):
        print(f"zoom session {i + 1}")
        print(df_zoom_not_correct_list[i])


if __name__ == '__main__':
     main()

