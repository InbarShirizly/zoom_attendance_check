import pytest
import sys
sys.path.append('../')
from server.parsing.attendance import Attendance
from server.parsing.utils import create_chat_df, create_students_df


chat_file_path = r"C:\Users\Inbar Shirizly\Documents\python\useful\ITC_programs\zoom_attendance_check\chat files\meeting_example_full_name.txt"
excel_file_path = r"C:\Users\Inbar Shirizly\Documents\python\useful\ITC_programs\zoom_attendance_check\student_csv_examples\example_data_already_prepared.xlsx"

df_students = create_students_df(file_name=excel_file_path.split("\\")[-1], file_data=excel_file_path)


@pytest.fixture()
def chat_file():
    with open(chat_file_path, "r", encoding="utf-8") as f:
        chat_df = create_chat_df(f.readlines())
    return chat_df



@pytest.mark.parametrize("chat_df", [chat_df])
@pytest.mark.parametrize("df_students", [df_students])
def test_first_message_time(chat_df, df_students):
        report = Attendance(chat_df, df_students, ['name', "id_number", "phone"], 1, "Attendance check", ["ITC", "Tech", "Challenge"])
        assert report.first_message_time.hour == 10