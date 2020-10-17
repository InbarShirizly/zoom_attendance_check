import pytest
import os

class TestParseClassFile:

    student_list_files = [
        ("example_mashov_file_edited_and_saved_97.xls", True, (17, 4)),
        ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True, (17, 4)),
        ("example_mashov_file_edited_and_saved_97_with_filled_data.xls", True, (17, 4)),
        ("example_csv_english_nba_8_students.csv", False, (8, 4)),
        ("example_excel_english_nba_7_students.xlsx", False, (7, 3)),
        ("example_excel_hebrew_7_students.xlsx", False, (7, 3)),
        ("example_excel_start_in_random_row.xlsx", False, (7, 3)),
        ("דוגמה לרשימת תלמידים.xlsx", False, (7, 3)),
        ("example_excel_english_nba_7_students_nonunique_id.xlsx", False, (7,3))
    ]

    @pytest.mark.parametrize(("excel_file_name", "expected_output", "df_shape"), student_list_files)
    def test_check_if_mashov_file(self, parser, folders, create_no_parse_df_students_func, excel_file_name, expected_output, df_shape):
        df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        assert parser.check_if_mashov_file(df_students) == expected_output

    @pytest.mark.parametrize(("excel_file_name", "if_is_mashov_file", "df_shape"), student_list_files)
    def test_mashov_file(self, parser, folders, excel_file_name, create_no_parse_df_students_func, student_full_columns, if_is_mashov_file, df_shape):
        df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        if parser.check_if_mashov_file(df_students):
            result_df = parser.mashov_file(df_students)
            assert result_df.shape == df_shape
            assert result_df.columns.isin(student_full_columns).all()
        else:
            assert True

    @pytest.mark.parametrize(("excel_file_name", "if_is_mashov_file", "df_shape"), student_list_files)
    def test_classic_file(self, parser, folders, excel_file_name, create_no_parse_df_students_func, student_full_columns, if_is_mashov_file, df_shape):
        df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        if not parser.check_if_mashov_file(df_students):
            result_df = parser.classic_file(df_students)
            assert result_df.shape == df_shape
            assert result_df.columns.isin(student_full_columns).all()
        else:
            assert True





