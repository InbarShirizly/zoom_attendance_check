import pytest
import os

class TestParseClassFile:

    class TestMashoveFiles:

        mashov_files_valid_data = [
            ("example_mashov_file_edited_and_saved_97.xls", True, 17),
            ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True, 17),
            ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True, 17),
            ("example_excel_english_nba_7_students.xlsx", False, 0),
            ("example_csv_english_nba_8_students.csv", False, 0),
            ("example_excel_start_in_random_row.xlsx", False, 0),
        ]

        @pytest.mark.parametrize(("excel_file_name", "expected_output", "num_records"), mashov_files_valid_data)
        def test_check_if_mashov_file(self, parser, folders, create_no_parse_df_students_func, excel_file_name, expected_output, num_records):
            df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
            assert parser.check_if_mashov_file(df_students) == expected_output

        @pytest.mark.parametrize(("excel_file_name", "if_is_mashov_file", "num_records"), mashov_files_valid_data)
        def test_mashov_file(self, parser, folders, excel_file_name, create_no_parse_df_students_func, student_full_columns, if_is_mashov_file, num_records):
            df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
            if parser.check_if_mashov_file(df_students):
                result_df = parser.mashov_file(df_students)
                assert result_df.shape[0] == num_records
                assert result_df.columns.isin(student_full_columns).all()
            else:
                assert True


    class TestBasicFiles:

        classic_files_data = [
            ("example_csv_english_nba_8_students.csv", 8),
            ("example_excel_english_nba_7_students.xlsx", 7),
            ("example_excel_hebrew_7_students.xlsx", 7),
            ("example_excel_start_in_random_row.xlsx", 7),
            ("דוגמה לרשימת תלמידים.xlsx", 7)
        ]

        @pytest.mark.parametrize(("excel_file_name", "num_records"), classic_files_data)
        def test_basic_file(self, parser, folders, excel_file_name, create_no_parse_df_students_func, student_full_columns, num_records):
            df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
            result_df = parser.classic_file(df_students)
            assert result_df.shape[0] == num_records
            assert result_df.columns.isin(student_full_columns).all()




