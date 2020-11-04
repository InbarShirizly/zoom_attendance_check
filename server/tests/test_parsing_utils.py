import pytest
import os


class TestChatAndStudent:

    chat_files_data_regular = [
        "chat_file_valid_english_nba_7_students.txt",
        "chat_file_valid_hebrew_7_students.txt"
    ]

    @pytest.mark.parametrize("chat_file_name",  chat_files_data_regular)
    def test_create_chat_df_validation_regular(self, folders, chat_df_func, chat_file_name):
        chat_df = chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))
        assert not chat_df.empty

    chat_files_data_empty = [
        "chat_file_empty.txt",
        "chat_file_not_structured.txt",
        "chat_file_not_structured_partially.txt",
    ]

    @pytest.mark.parametrize("chat_file_name", chat_files_data_empty)
    def test_create_chat_df_validation_empty(self, folders, chat_df_func, chat_file_name):
        with pytest.raises(ValueError):
            assert chat_df_func(os.path.join(folders["chat_files_folder"], chat_file_name))


    student_list_files_data = [
        "example_csv_english_nba_8_students.csv",
        "example_excel_english_nba_7_students.xlsx",
        "example_excel_hebrew_7_students.xlsx",
        "example_excel_start_in_random_row.xlsx",
        "example_mashov_file_edited_and_saved_97.xls",
        "example_mashov_file_edited_and_saved_97_with_filled_data.xls",
        "דוגמה לרשימת תלמידים.xlsx",
    ]

    @pytest.mark.parametrize("excel_file_name", student_list_files_data)
    def test_create_students_df_validation(self, folders, create_no_parse_df_students_func, excel_file_name):
        df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        assert not df_students.empty

    student_list_files_data_problems = [
        "example_mashov_file_empty.xls",
        "example_excel_too_much_records.xlsx"
    ]

    @pytest.mark.parametrize("excel_file_name", student_list_files_data_problems)
    def test_create_students_df_validation_problem(self, folders, create_no_parse_df_students_func, excel_file_name):
        with pytest.raises(ValueError):
            assert create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))


