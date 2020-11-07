import pytest
import os

from src.parsing.attendance import Attendance
from src.parsing import AttendanceMetaData


class TestAttendance:
    chat_files_data = [
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"]),
        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 1, "Attendance check", ["Roei teacher", "Elad Visitor"])
    ]

    @pytest.mark.parametrize(("chat_file_name", "excel_file_name", "time_delta", "start_sentence", "zoom_names_to_ignore"), chat_files_data)
    def test_first_message_time(self, folders, chat_df_func, df_students_func, filter_modes,
                                chat_file_name, excel_file_name, time_delta, start_sentence, zoom_names_to_ignore):
        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        student_df = df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        report = Attendance(chat_df, student_df, filter_modes, time_delta, start_sentence, zoom_names_to_ignore)
        assert report.first_message_time.hour == 10
        assert report.first_message_time.minute == 46
        assert report.first_message_time.second == 16

    chat_files_start_indices = [
        ("chat_file_valid_hebrew_7_students.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], 3),
        ("chat_file_valid_hebrew_7_students.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Idan Aviv"], 4),
        ("chat_file_valid_hebrew_7_students.txt", 1, "check", ["Roei teacher"], 0),
        ("chat_file_valid_english_nba_7_students.txt", 1, "Attendance check", ["Roei teacher", "Elad Visitor"], 3)
    ]

    @pytest.mark.parametrize(("chat_file_name", "time_delta", "start_sentence", "zoom_names_to_ignore", "num_sessions"), chat_files_start_indices)
    def test_get_start_indices(self, folders, chat_df_func, filter_modes,
                               chat_file_name, time_delta, start_sentence, zoom_names_to_ignore, num_sessions):
        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        assert len(start_indices) == num_sessions

    chat_files_time_segment_rows = [
        ("chat_file_valid_hebrew_7_students.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [5, 7, 6]),
        ("chat_file_valid_hebrew_7_students.txt", 1, "בדיקת נוכחות", ["Roei teacher", "Idan Aviv"], [5, 7, 3, 3]),
        ("chat_file_valid_hebrew_7_students.txt", 1, "check", ["Roei teacher"], 0),
        ("chat_file_valid_hebrew_7_students.txt", 3, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [6, 9, 6]),
        ("chat_file_valid_english_nba_7_students.txt", 1, "Attendance check", ["Roei teacher", "Elad Visitor"], [5, 7, 6])
    ]

    @pytest.mark.parametrize(("chat_file_name", "time_delta",
                              "start_sentence", "zoom_names_to_ignore", "list_rows_in_session"),
                                chat_files_time_segment_rows)
    def test_get_df_of_time_segment(self, folders, chat_df_func, df_students_func, filter_modes,
                               chat_file_name, time_delta, start_sentence, zoom_names_to_ignore, list_rows_in_session):
        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(chat_df, start_indices, ind, time_delta)
            assert df_session.shape[0] == list_rows_in_session[ind]


    chat_files_status_test = [
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 0, 0]),
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 2, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 0, 1]),
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 4, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 1, 1]),
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 5, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"], [1, 1, 2, 1, 1, 2, 1]),
        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 1, "Attendance check", ["Roei teacher", "Elad Visitor"], [1, 2, 0, 1, 2, 0, 1]),
        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 3, "Attendance check", ["Roei teacher", "Elad Visitor"], [1, 2, 0, 1, 2, 1, 1]),
        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 5, "Attendance check", ["Roei teacher", "Elad Visitor"], [1, 2, 1, 1, 2, 1, 1])

    ]

    @pytest.mark.parametrize(
        ("chat_file_name", "excel_file_name", "time_delta", "start_sentence", "zoom_names_to_ignore", "status_list"),
        chat_files_status_test)
    def test_student_status_table(self, folders, chat_df_func, df_students_func, filter_modes,
                               chat_file_name, excel_file_name, time_delta, start_sentence, zoom_names_to_ignore, status_list):
        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        student_df = df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        attendance = Attendance(chat_df, student_df, filter_modes, time_delta, start_sentence, zoom_names_to_ignore)
        students_status = attendance.student_status_table(1)  # passing classroom number (is 1 in the tests)
        assert (students_status['status'] == status_list).all()