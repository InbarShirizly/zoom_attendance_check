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

import os
from datetime import datetime, timedelta
import pandas as pd
from difflib import get_close_matches
import json
import re
import conf


def get_content_df(chat_path):
    """
    convert the chat text file to a data frame
    :param chat_path: the path of the relevant chat file (str)
    :return: data frame with the data from the chat
    """
    with open(chat_path, "r", encoding="utf-8") as file:
        data = [re.search(conf.CHAT_PATTERN, line).groups() for line in file if re.match(conf.CHAT_PATTERN, line)]
    return pd.DataFrame(data, columns=conf.COLUMNS_NAMES)


def get_indexes_of_start_attend_check(df_chat):
    """
    find all sessions of attendance check
    :param df_chat: data frame with the data from the chat
    :return: indexes in the df when the attendance check started (list of int)
    """
    df_chat["time"] = df_chat["time"].apply(lambda string: datetime.strptime(string, "%H:%M:%S"))
    return df_chat.index[df_chat['chat'].apply(lambda string: conf.SENTENCE_START.lower() in string.lower())]


def get_list_of_participants(df_chat, start_index):
    """
    parse the data frame of the chat data to find the participants in the meeting that
    wrote something in a period of time before or after a specific sentence had been writen
    zoom user with name that will be probably the lecturer is deleted
    :param df_chat: data frame of the chat content
    :param start_index: start index of session
    :return: participants in the zoom meeting (exclude lecturer) - (list_
    """

    time_segment_start = df_chat.loc[start_index, "time"]
    filt = (df_chat["time"] >= time_segment_start - conf.TIME_DELTA) & \
           (df_chat["time"] <= time_segment_start + conf.TIME_DELTA)

    participants_list = sorted(df_chat.loc[filt, "users"].unique().tolist(), key=lambda word: word[0].lower())
    # find and delete lecturer from the list
    participants_list_final = participants_list.copy()

    for student in participants_list:
        for phrase in conf.WORDS_FOR_NOT_INCLUDED_PARTICIPATORS:
            if phrase in student:
                participants_list_final.remove(student)
                break

    return participants_list_final


def find_student_full_names(zoom_participants):
    """
    converts zoom names of participants to their full name using
    a list that contains all their names.
    first, check in the json file that already contains names from previous sessions
    if they don't appear, use diflib func to find the match - full name for the participator
    :param zoom_participants: list of all participants parsed
    :return: list of all participants full names
    """
    try:
        with open(conf.JSON_FILE_NAME, "r") as json_file:
            zoom_names_dict = json.load(json_file)
    except FileNotFoundError:
        zoom_names_dict = {}

    class_first_names = [name.split(" ")[0] for name in conf.class_names]
    students_in_zoom_full_name = []
    for student in zoom_participants:
        if student in zoom_names_dict:
            students_in_zoom_full_name.append(zoom_names_dict[student])
        else:
            options = get_close_matches(student.split(" ")[0].title(), class_first_names, n=3, cutoff=0.95)
            if len(options) == 0:
                options = get_close_matches(student.split(" ")[-1].title(), class_first_names, n=3, cutoff=0.95)
            if len(options) > 1:
                relevant_full_names = [student for student in conf.class_names if options[0] in student]
                for relevant_student in relevant_full_names:
                    if relevant_student.split(" ")[-1][0].upper() == student.split(" ")[-1][0].upper():
                        students_in_zoom_full_name.append(relevant_student)
            else:
                students_in_zoom_full_name.append([student.title() for student in conf.class_names if options[0] in student][0])
    return students_in_zoom_full_name


def add_zoom_name_to_fullname_json(zoom_participants_list, full_names_participants_list):
    """
    create or update json file contains conversion between zoom names to full names
    :param zoom_participants_list: zoom names (list)
    :param full_names_participants_list: full names of student (list)
    """
    try:
        with open(conf.JSON_FILE_NAME, "r") as json_file:
            zoom_names_dict = json.load(json_file)
    except FileNotFoundError:
        zoom_names_dict = {}

    for zoon_name, full_name in zip(zoom_participants_list, full_names_participants_list):
        if zoon_name not in zoom_names_dict:
            zoom_names_dict[zoon_name] = full_name

    with open(conf.JSON_FILE_NAME, "w") as json_file:
        json.dump(zoom_names_dict, json_file, indent=2)


def main():
    df = get_content_df(conf.FILE_NAME)
    attend_indexes = get_indexes_of_start_attend_check(df)

    for session, index_in_df in enumerate(attend_indexes):
        participants_list = get_list_of_participants(df, index_in_df)
        full_names_participants_list = find_student_full_names(participants_list)

        # find the missing students - subtracting from the full list the participators
        missing_students = sorted(set(conf.class_names) - set(full_names_participants_list))
        print(f"text file: {conf.FILE_NAME}, session {session + 1},  missing students: {missing_students}")

        # update json file with connection between zoom name and full names
        add_zoom_name_to_fullname_json(participants_list, full_names_participants_list)

if __name__ == '__main__':
     main()

