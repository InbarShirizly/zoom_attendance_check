import pytest
import sys
sys.path.append('../')
from server.parsing.utils import create_chat_df, create_students_df
import os

# TODO: need to load the file as FileStorage type and then start testing

@pytest.fixture
def folders():
    CHAT_FILES_FOLDER = "./files_to_test/chat_files"
    STUDENT_EXCEL_FILES_FOLDER = "./files_to_test/students_list_excel"
    return {"chat_folder": CHAT_FILES_FOLDER, "student_list_folder": STUDENT_EXCEL_FILES_FOLDER}

student_list_files_data = [
        ("example_csv.csv", True),
        ("example_csv_2.csv", True),
        ("example_csv_3.csv", True),
        ("example_csv_4.csv", True),
        ("example_excel.xlsx", True),
        ("example_excel_start_in_random_row.xlsx", True),
        ("example_mashov_file_edited_and_saved_97.xls", True),
        ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True),
        ("רשימה מקורית.xls", True),
]

student_list_files_data_problems = [
        "example_mashov_file_empty.xls",
        "example_excel_too_much_records.xlsx"
]

class TestChatAndStudent:

    chat_files_data_regular = [
        ("chat_file_valid.txt", False)
    ]

    @pytest.mark.parametrize(("file_name", "expected_output"),  chat_files_data_regular)
    def test_create_chat_df_validation_regular(self, folders, file_name, expected_output):
        with open(os.path.join(folders["chat_folder"], file_name), "r", encoding="utf-8") as f:
            chat_df = create_chat_df(f.readlines())
        assert chat_df.empty == expected_output

    chat_files_data_empty = [
        ("chat_file_empty.txt", True),
        ("chat_file_not_structured.txt", True),
        ("chat_file_not_structured_partially.txt", True),
    ]

    @pytest.mark.parametrize(("file_name", "expected_output"), chat_files_data_empty)
    def test_create_chat_df_validation_empty(self, folders, file_name, expected_output):
        with open(os.path.join(folders["chat_folder"], file_name), "r", encoding="utf-8") as f:
            with pytest.raises(ValueError):
                assert create_chat_df(f.readlines())


    @pytest.mark.parametrize(("file_name", "expected_output"), student_list_files_data)
    def test_create_students_df_validation(self, folders, file_name, expected_output):
        df_students = create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))
        assert not df_students.empty == expected_output

    @pytest.mark.parametrize("file_name", student_list_files_data_problems)
    def test_create_students_df_validation_problem(self, folders, file_name):
        with pytest.raises(ValueError):
            assert create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))


