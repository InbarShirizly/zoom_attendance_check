import pytest
import sys
sys.path.append('../')
from server.parsing.utils import create_chat_df, create_students_df, validate_file_content
import os


@pytest.fixture
def folders():
    CHAT_FILES_FOLDER = "./files_to_test/chat_files"
    STUDENT_EXCEL_FILES_FOLDER = "./files_to_test/students_list_excel"
    return {"chat_folder": CHAT_FILES_FOLDER, "student_list_folder": STUDENT_EXCEL_FILES_FOLDER}


chat_files_data = [
        ("chat_file_empty.txt", True),
        ("chat_file_not_structured.txt", True),
        ("chat_file_not_structured_partially.txt", True),
        ("chat_file_valid.txt", False)
]


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
    @pytest.mark.parametrize(("file_name", "expected_output"),  chat_files_data)
    def test_create_chat_df_validation(self, folders, file_name, expected_output):
        with open(os.path.join(folders["chat_folder"], file_name), "r", encoding="utf-8") as f:
            chat_df = create_chat_df(f.readlines())
        assert chat_df.empty == expected_output

    @pytest.mark.parametrize(("file_name", "expected_output"), student_list_files_data)
    def test_create_students_df_validation(self, folders, file_name, expected_output):
        df_students = create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))
        assert validate_file_content(df_students)

    @pytest.mark.parametrize("file_name", student_list_files_data_problems)
    def test_create_students_df_validation_problem(self, folders, file_name):
        df_students = create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))
        with pytest.raises(ValueError):
            validate_file_content(df_students)


