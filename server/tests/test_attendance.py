import pytest
import sys

sys.path.append('../')
from server.parsing.attendance import Attendance
from server.parsing.utils import create_chat_df, create_students_df
import os
from server.config import ParseConfig
from server.parsing.parse_class_file import ParseClassFile
from server.parsing import AttendanceMetaData


@pytest.fixture(scope="module")
def folders():
    CHAT_FILES_FOLDER = "./files_to_test/chat_files"
    STUDENT_EXCEL_FILES_FOLDER = "./files_to_test/students_list_excel"
    return {"chat_folder": CHAT_FILES_FOLDER, "student_list_folder": STUDENT_EXCEL_FILES_FOLDER}


@pytest.fixture(scope="module")
def student_df(folders):
    file_name = "example_excel.xlsx"
    file_ext = "." + file_name.split(".")[-1]
    df_students = create_students_df(file_ext, os.path.join(folders["student_list_folder"], file_name))
    parser = ParseClassFile.from_object(ParseConfig)
    student_df = parser.parse_df(df_students)
    # add index manually because in the real function it parser the df from the database
    student_df["id"] = [i for i in range(1, student_df.shape[0] + 1)]
    return student_df


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


class TestAttendance:
    chat_files_data = [
        ("chat_file_valid.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"])
    ]

    @pytest.mark.parametrize(("file_name", "time_delta", "start_sentence", "zoom_names_to_ignore"), chat_files_data)
    def test_first_message_time(self, folders, student_df, chat_df_func, filter_modes,
                                file_name, time_delta, start_sentence, zoom_names_to_ignore):
        chat_df = chat_df_func(os.path.join(folders["chat_folder"], file_name))
        report = Attendance(chat_df, student_df, filter_modes, time_delta, start_sentence, zoom_names_to_ignore)
        assert report.first_message_time.hour == 10
        assert report.first_message_time.minute == 46
        assert report.first_message_time.second == 16

    chat_files_start_indices = [
        ("chat_file_valid.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], 3),
        ("chat_file_valid.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Idan Aviv"], 4),
        ("chat_file_valid.txt", 1, "check", ["Roei teacher"], 0)
    ]

    @pytest.mark.parametrize(("file_name", "time_delta", "start_sentence", "zoom_names_to_ignore", "num_sessions"), chat_files_start_indices)
    def test_get_start_indices(self, folders, student_df, chat_df_func, filter_modes,
                               file_name, time_delta, start_sentence, zoom_names_to_ignore, num_sessions):
        chat_df = chat_df_func(os.path.join(folders["chat_folder"], file_name))
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        assert len(start_indices) == num_sessions

    chat_files_time_segment_rows = [
        ("chat_file_valid.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [5, 7, 6]),
        ("chat_file_valid.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Idan Aviv"], [5, 7, 3, 3]),
        ("chat_file_valid.txt", 1, "check", ["Roei teacher"], 0),
        ("chat_file_valid.txt", 3, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [6, 9, 6]),
    ]

    @pytest.mark.parametrize(("file_name", "time_delta", "start_sentence", "zoom_names_to_ignore", "list_rows_in_session"), chat_files_time_segment_rows)
    def test_get_df_of_time_segment(self, folders, student_df, chat_df_func, filter_modes,
                               file_name, time_delta, start_sentence, zoom_names_to_ignore, list_rows_in_session):
        chat_df = chat_df_func(os.path.join(folders["chat_folder"], file_name))
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(chat_df, start_indices, ind, time_delta)
            assert df_session.shape[0] == list_rows_in_session[ind]


    chat_files_status_test = [
        ("chat_file_valid.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 0, 0]),
        ("chat_file_valid.txt", 2, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 0, 1]),
        ("chat_file_valid.txt", 4, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 1, 1]),
        ("chat_file_valid.txt", 5, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 2, 1])
        ]

    @pytest.mark.parametrize(
        ("file_name", "time_delta", "start_sentence", "zoom_names_to_ignore", "status_list"),
        chat_files_status_test)
    def test_student_status_table(self, folders, student_df, chat_df_func, filter_modes,
                               file_name, time_delta, start_sentence, zoom_names_to_ignore, status_list):
        chat_df = chat_df_func(os.path.join(folders["chat_folder"], file_name))
        attendance = Attendance(chat_df, student_df, filter_modes, time_delta, start_sentence, zoom_names_to_ignore)
        students_status = attendance.student_status_table(1)
        assert (students_status['status'] == status_list).all()