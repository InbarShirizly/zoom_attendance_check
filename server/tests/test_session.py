import pytest
import sys

sys.path.append('../')
from server.parsing.attendance import Attendance
from server.config import ParseConfig
from server.parsing.parse_class_file import ParseClassFile
from server.parsing.utils import create_chat_df, create_students_df
import os
from server.parsing import AttendanceMetaData
from server.parsing.session import Session


@pytest.fixture(scope="module")
def folders():
    CHAT_FILES_FOLDER = "./files_to_test/chat_files"
    STUDENT_EXCEL_FILES_FOLDER = "./files_to_test/students_list_excel"
    return {"chat_folder": CHAT_FILES_FOLDER, "student_list_folder": STUDENT_EXCEL_FILES_FOLDER}


@pytest.fixture(scope="module")
def df_students_func(folders):
    def arrange_df_students(file_name):
        file_ext = "." + file_name.split(".")[-1]
        df_students = create_students_df(file_ext, os.path.join(folders["student_list_folder"], file_name))
        parser = ParseClassFile.from_object(ParseConfig)
        student_df = parser.parse_df(df_students)
        # add index manually because in the real function it parser the df from the database
        student_df["id"] = [i for i in range(1, student_df.shape[0] + 1)]
        return student_df
    return arrange_df_students


@pytest.fixture(scope="module")
def chat_df_func():
    def arrange_chat_df(chat_path):
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_df = create_chat_df(f.readlines())
        return chat_df
    return arrange_chat_df


@pytest.fixture(scope="module")
def filter_modes():
    return ["phone", "id_number", "name", "org_class", "gender"]


class TestSession:

    chat_files_data_session_start_time = [
        ("chat_file_valid.txt", "example_excel.xlsx", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         [(10, 46, 16), (10, 57, 22), (11, 57, 16)]),

        ("chat_file_valid.txt", "example_excel.xlsx", 5, "בדיקת נוכחות", ["Idan Aviv"],
         [(11, 57, 45)]),

        ("chat_file_valid_english_nba.txt", "example_excel_english.xlsx", 1, "Attendance check", ["Roei teacher", "Elad Visitor"],
         [(10, 46, 16), (10, 57, 22), (11, 57, 16)])

    ]

    @pytest.mark.parametrize(("chat_file_name", "excel_file_name", "time_delta", "start_sentence",
                              "zoom_names_to_ignore", "message_time_tuples_list"), chat_files_data_session_start_time)
    def test_first_message_time(self, folders, chat_df_func, df_students_func, filter_modes,
                                chat_file_name, excel_file_name, time_delta, start_sentence, zoom_names_to_ignore, message_time_tuples_list):
        chat_df = chat_df_func(os.path.join(folders["chat_folder"], chat_file_name))
        student_df = df_students_func(excel_file_name)
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)

        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        df_students_for_report = student_df.set_index("id").astype(str).reset_index()

        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(chat_df, start_indices, ind, time_delta)
            current_session = Session(df_students_for_report, df_session, meta_data)
            assert current_session._first_message_time.hour == message_time_tuples_list[ind][0]
            assert current_session._first_message_time.minute == message_time_tuples_list[ind][1]
            assert current_session._first_message_time.second == message_time_tuples_list[ind][2]


    chat_files_data_session = [
        ("chat_file_valid.txt", "example_excel.xlsx", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (4, 6, 4), "relevant_messages": (3, 4, 2)}),

        ("chat_file_valid.txt", "example_excel.xlsx", 3, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (5, 8, 4), "relevant_messages": (4, 5, 2)}),

        ("chat_file_valid.txt", "example_excel.xlsx", 5, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (6, 9, 5), "relevant_messages": (5, 6, 3)}),

        ("chat_file_valid.txt", "example_excel.xlsx", 5, "בדיקת נוכחות", ["Idan Aviv"],
         {"total_messages": ([3]), "relevant_messages": ([2])}),

        ("chat_file_valid_english_nba.txt", "example_excel_english.xlsx", 1, "Attendance check", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (4, 6, 4), "relevant_messages": (3, 4, 3)})
    ]

    @pytest.mark.parametrize(("chat_file_name", "excel_file_name", "time_delta", "start_sentence",
                              "zoom_names_to_ignore", "counting_dict"), chat_files_data_session)
    def test_get_relevant_chat_in_session(self, folders, chat_df_func, df_students_func, filter_modes,
                                chat_file_name, excel_file_name, time_delta, start_sentence, zoom_names_to_ignore, counting_dict):

        chat_df = chat_df_func(os.path.join(folders["chat_folder"], chat_file_name))
        student_df = df_students_func(excel_file_name)
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        df_students_for_report = student_df.set_index("id").astype(str).reset_index()

        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(chat_df, start_indices, ind, time_delta)
            session_part = Session.get_relevant_chat_in_session(df_students_for_report, df_session, meta_data)
            assert session_part.shape[0] == counting_dict["total_messages"][ind]
            assert (session_part["relevant"] == 1).sum() == counting_dict["relevant_messages"][ind]