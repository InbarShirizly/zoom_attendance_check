import pytest
import sys
sys.path.append('../')
from server.parsing.parse_class_file import ParseClassFile
from server.parsing.utils import create_students_df
from server.config import ParseConfig
import os


@pytest.fixture(scope="module")
def folders():
    CHAT_FILES_FOLDER = "./files_to_test/chat_files"
    STUDENT_EXCEL_FILES_FOLDER = "./files_to_test/students_list_excel"
    return {"chat_folder": CHAT_FILES_FOLDER, "student_list_folder": STUDENT_EXCEL_FILES_FOLDER}

@pytest.fixture(scope="module")
def parser():
    return ParseClassFile.from_object(ParseConfig)


@pytest.fixture(scope="module")
def student_full_columns_columns(parser, folders):
    return ["id", "phone", "id_number", "name", "org_class", "gender"]


class TestParseClassFile:

    class TestMashoveFiles:


        mashov_files_valid_data = [
            ("רשימה מקורית.xls", True, 17),
            ("example_mashov_file_edited_and_saved_97.xls", True, 17),
            ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True, 17),
            ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True, 17),
            ("example_mashov_file_empty.xls", False, 0),
            ("example_excel.xlsx", False, 0),
            ("example_excel_start_in_random_row.xlsx", False, 0),
        ]


        @pytest.mark.parametrize(("file_name", "expected_output", "num_records"), mashov_files_valid_data)
        def test_check_if_mashov_file(self, parser, folders, file_name, expected_output, num_records):
            df_students = create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))
            assert parser.check_if_mashov_file(df_students) == expected_output

        @pytest.mark.parametrize(("file_name", "if_is_mashov_file", "num_records"), mashov_files_valid_data)
        def test_mashov_file(self, parser, folders, file_name, student_full_columns_columns, if_is_mashov_file, num_records):
            df_students = create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))
            if parser.check_if_mashov_file(df_students):
                result_df = parser.mashov_file(df_students)
                assert result_df.shape[0] == num_records
                assert result_df.columns.isin(student_full_columns_columns).all()
            else:
                assert True


    class TestBasicFiles:


        classic_files_data = [
            ("example_csv.csv", 8),
            ("example_csv_2.csv", 7),
            ("example_csv_2.csv", 7),
            ("example_excel.xlsx", 7),
            ("example_excel_start_in_random_row.xlsx", 7),
            ("דוגמה לרשימת תלמידים.xlsx", 7)
        ]

        @pytest.mark.parametrize(("file_name", "num_records"), classic_files_data)
        def test_basic_file(self, parser, folders, file_name, student_full_columns_columns, num_records):
            df_students = create_students_df(file_name, os.path.join(folders["student_list_folder"], file_name))
            result_df = parser.classic_file(df_students)
            assert result_df.shape[0] == num_records
            assert result_df.columns.isin(student_full_columns_columns).all()




