import string


class FlaskConfig:
    SECRET_KEY = 'TEMP_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    STORE_CHAT = False # if this variable is True, all the chat, session and zoom names data from a report will be store in the datbase. currently not supported


class ParseConfig:
    FILE_COLS_DICT = {
        "name": ["תלמיד", "שמות", "שם", "סטודנט", "name", "student"],
        "id_number": ["תעודת זהות", "תז", "id"],
        "phone": ["טלפון", "phone"],
        "gender": ["מין", "gender"],
        "org_class": ["כיתה", "class"]
    }
    MASHOV_COLS = ["name", "org_class", "id_number"]
    GENDER_DICT = {1: ["זכר", "ז", "m", "male"], 0: ["נקבה", "נ", "f", "female"]}
    DELETE_ROWS_CONTAIN = ["הופק בתאריך"]
    UNIQUE_COLUMNS_RESTRICTION = ["phone", "id_number", "name", "country", "country_code"]


class ValidatorsConfig:
    INVALID_USERNAME_CHARS = string.punctuation
    MIN_PASSWORD_LEN = 4
    REQUIRED_PASSWORD_CHARS = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    CHAT_FILE_EXT = [".txt"]
    STUDENTS_FILE_EXT = [".xls", ".xlsx", ".csv"]
    MAX_CLASSROOMS = 10  # Max classrooms per students
    MAX_REPORTS = 7  # Max reports per classroom
    MAX_STUDENTS_IN_CLASS = 200

class RestErrors:
    INVALID_ROUTE = "route_doesn't_exists"
    INVALID_CLASS = "invalid_class_id"
    INVALID_REPORT = "invalid_report_id"
    INVALID_STATUS = "invalid_status_id"
    USERNAME_TAKEN = "username_taken"
    EMAIL_TAKEN = "email_taken"
    ILLEGAL_USERNAME_CHARS = "username_contains_illegal_chars" 
    PASSWORD_TO_SHORT = 'passowrd_to_short'
    PASSWORD_MUST_CONTAIN = "password_dosen't_contain_required_chars"
    INVALID_TIME_DELTA = "invalid_time_delta"
    INVALID_STUDENTS_FILE = "invalid_student_file"
    INVALID_CHAT_FILE = "invalid_chat_file"
    INVALID_CREDENTIALS = "credentials_invalid"
    INVALID_TOKEN = "token_invalid"
    TOKEN_EXPIRED = "token_expired"
    MAX_REPORTS = "to_many_reports"
    MAX_CLASSROOMS = "to_many_classrooms"
    TO_MANY_RECORDS = "to_many_records"
    INVALID_TIME_STAMP = 'invalid_time_stamp'
    INVALID_STUDENT_ID = "invalid_student_id"
    
class SerializeConfig:
    LOGIN_SALT = 'login'
    LOIGN_TOKEN_AGE = 604800 # Week in seconds