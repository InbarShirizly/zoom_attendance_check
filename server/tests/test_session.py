import pytest
import os
from server.parsing.attendance import Attendance
from server.parsing import AttendanceMetaData
from server.parsing.session import Session


class TestSession:

    chat_files_data_session_start_time = [
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         [(10, 46, 16), (10, 57, 22), (11, 57, 16)]),

        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 5, "בדיקת נוכחות", ["Idan Aviv"],
         [(11, 57, 45)]),

        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 1, "Attendance check", ["Roei teacher", "Elad Visitor"],
         [(10, 46, 16), (10, 57, 22), (11, 57, 16)])

    ]

    @pytest.mark.parametrize(("chat_file_name", "excel_file_name", "time_delta", "start_sentence",
                              "zoom_names_to_ignore", "message_time_tuples_list"), chat_files_data_session_start_time)
    def test_first_message_time(self, folders, chat_df_func, df_students_func, filter_modes,
                                chat_file_name, excel_file_name, time_delta, start_sentence, zoom_names_to_ignore, message_time_tuples_list):
        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        student_df = df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
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
        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 1, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (4, 6, 4), "relevant_messages": (3, 4, 2)}),

        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 3, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (5, 8, 4), "relevant_messages": (4, 5, 2)}),

        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 5, "בדיקת נוכחות", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (6, 9, 5), "relevant_messages": (5, 6, 3)}),

        ("chat_file_valid_hebrew_7_students.txt", "example_excel_hebrew_7_students.xlsx", 5, "בדיקת נוכחות", ["Idan Aviv"],
         {"total_messages": ([3]), "relevant_messages": ([2])}),

        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 1, "Attendance check", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (4, 6, 4), "relevant_messages": (3, 4, 3)}),

        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 3,  "Attendance check", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (5, 8, 4), "relevant_messages": (4, 5, 3)}),

        ("chat_file_valid_english_nba_7_students.txt", "example_excel_english_nba_7_students.xlsx", 5,  "Attendance check", ["Roei teacher", "Elad Visitor"],
         {"total_messages": (6, 9, 5), "relevant_messages": (5, 6, 4)})
    ]

    @pytest.mark.parametrize(("chat_file_name", "excel_file_name", "time_delta", "start_sentence",
                              "zoom_names_to_ignore", "counting_dict"), chat_files_data_session)
    def test_get_relevant_chat_in_session(self, folders, chat_df_func, df_students_func, filter_modes,
                                chat_file_name, excel_file_name, time_delta, start_sentence, zoom_names_to_ignore, counting_dict):

        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        student_df = df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        meta_data = AttendanceMetaData(filter_modes=filter_modes, time_delta=time_delta,
                                       start_sentence=start_sentence, zoom_names_to_ignore=zoom_names_to_ignore)
        start_indices = Attendance.get_start_indices(chat_df, meta_data)
        df_students_for_report, report_df = Attendance.prepare_chat_and_classroom(student_df, chat_df)

        for ind in range(len(start_indices)):
            df_session = Attendance.get_df_of_time_segment(chat_df, start_indices, ind, time_delta)
            session_part = Session.get_relevant_chat_in_session(df_students_for_report, df_session, meta_data)
            assert session_part.shape[0] == counting_dict["total_messages"][ind]
            assert (session_part["relevant"] == 1).sum() == counting_dict["relevant_messages"][ind]