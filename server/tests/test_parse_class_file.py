import pytest
import os
import numpy as np

@pytest.fixture(scope="module")
def create_students_with_nonunique():
    def arrange_df_students_with_nonunique(df_students):
        print(df_students)
        return df_students
    return arrange_df_students_with_nonunique



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

    @pytest.mark.parametrize(("excel_file_name", "if_is_mashov_file", "df_shape"), student_list_files)
    def test_check_filter_columns_unique(self, parser, folders, excel_file_name, create_no_parse_df_students_func, student_full_columns, if_is_mashov_file, df_shape):
        df_students = create_no_parse_df_students_func(os.path.join(folders["student_list_files_folder"], excel_file_name))
        if parser.check_if_mashov_file(df_students):
            result_df = parser.mashov_file(df_students)
        else:
            result_df = parser.classic_file(df_students)

        new_row = {"name": "check name", "org_class": "A2", "id_number": "111111111", "gender": 1, "phone": 528702485}
        chosen_col = np.random.choice([col for col in result_df.columns if col in parser._unique_columns_restriction])
        non_unique_value = result_df[chosen_col].sample(1).iloc[0]
        new_row[chosen_col] = non_unique_value
        result_df.loc[len(result_df)] = [new_row[col] for col in result_df.columns]

        with pytest.raises(ValueError):
            assert parser.check_filter_columns_unique(result_df)



