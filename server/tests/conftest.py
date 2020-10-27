import pytest
from server.parsing.parse_class_file import ParseClassFile
from server.config import ParseConfig
from server.parsing.utils import create_students_df, create_chat_df


@pytest.fixture
def folders():
    chat_files_folder = "server/tests/files_to_test/chat_files"
    student_list_files_folder = "server/tests/files_to_test/students_list_excel"
    return {"chat_files_folder": chat_files_folder, "student_list_files_folder": student_list_files_folder}


@pytest.fixture
def student_full_columns(parser, folders):
    return ["id", "phone", "id_number", "name", "org_class", "gender", "country", "country_code"]

@pytest.fixture
def filter_modes():
    return ["phone", "id_number", "name"]

@pytest.fixture
def parser():
    return ParseClassFile.from_object(ParseConfig)


@pytest.fixture
def create_no_parse_df_students_func():
    def arrange_df_students_before_parsing(students_list_path):
        file_ext = "." + students_list_path.split(".")[-1]
        df_students = create_students_df(file_ext, students_list_path)
        return df_students
    return arrange_df_students_before_parsing


@pytest.fixture
def df_students_func():
    def arrange_df_students(students_list_path):
        file_ext = "." + students_list_path.split(".")[-1]
        df_students = create_students_df(file_ext, students_list_path)
        parser = ParseClassFile.from_object(ParseConfig)
        student_df = parser.parse_df(df_students)
        # add index manually because in the real function it parser the df from the database
        student_df["id"] = [i for i in range(1, student_df.shape[0] + 1)]
        return student_df
    return arrange_df_students


@pytest.fixture
def chat_df_func():
    def arrange_chat_df(chat_path):
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_df = create_chat_df(f.readlines())
        return chat_df
    return arrange_chat_df

