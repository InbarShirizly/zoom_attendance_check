from server import db, bcrypt
from server.models.orm import TeacherModel
from server.config import RestErrors
import email_validator
from datetime import datetime
import os
from werkzeug.datastructures import FileStorage
from server.parsing import parser
from server.parsing.utils import create_chat_df, create_students_df


# The class is responsible for validating diffrent inputs to the API
class Validators:
    def __init__(self, supported_chat_file_ext, supported_student_files_ext, max_students_in_class,
                 invalid_username_chars="", min_password_len=0, required_password_chars=[]):
        #TODO: documentation
        self._supported_chat_file_ext = supported_chat_file_ext
        self._supported_student_files_ext = supported_student_files_ext
        self._max_students_in_class = max_students_in_class
        self._invalid_username_chars = invalid_username_chars
        self._min_password_len = min_password_len
        self._required_password_chars = required_password_chars

    @classmethod
    def from_object(cls, config):
        """
        The function will init an instance from config object
        """
        return cls(
            config.CHAT_FILE_EXT,
            config.STUDENTS_FILE_EXT,
            config.MAX_STUDENTS_IN_CLASS,
            config.INVALID_USERNAME_CHARS,
            config.MIN_PASSWORD_LEN,
            config.REQUIRED_PASSWORD_CHARS
        )

    def username(self, value):
        """
        The function will validate username (Make sure the username is unique and that he doesn't contain illegal chars)
        :param value: the username value to check (str)
        :return: username if valid (str)
        """
        value = str(value)
        if TeacherModel.query.filter_by(username=value).first():
            raise ValueError(RestErrors.USERNAME_TAKEN)
        if Validators.any_of_chars_match(self._invalid_username_chars, value):
            raise ValueError(RestErrors.ILLEGAL_USERNAME_CHARS)
        return value

    def email(self, value):
        """
        The function will make sure the email is in the correct format and unique 
        :param value: the email value to check (str)
        :return: email if valid (str)
        """
        value = str(value)
        if TeacherModel.query.filter_by(email=value).first():
            raise ValueError(RestErrors.EMAIL_TAKEN)
        return email_validator.validate_email(value).email

    def password(self, value):
        """
        The function will check if the password is valid (Containing at least one of each required char groups, longer than the min length)
        :param value: the password to check (str)
        :return: hashed password to store in the db (str)
        """
        value = str(value)
        if len(value) < self._min_password_len:
            raise ValueError(RestErrors.PASSWORD_TO_SHORT)
        for chars_list in self._required_password_chars:
            if not Validators.any_of_chars_match(chars_list, value):
                raise ValueError(RestErrors.PASSWORD_MUST_CONTAIN)
        return bcrypt.generate_password_hash(value).decode('utf-8')

    def date(self, value):
        """
        The function will check that the date is given in the correct format
        :param value: the input unix timestamp (integer)
        :return value: the date (datetime)
        """
        try:
            value = int(value)
            return datetime.fromtimestamp(value)
        except:
            raise ValueError(RestErrors.INVALID_TIME_STAMP)
        
    def students_file(self, value):
        """
        The function will make sure the student file has the right extenstion
        :param value: the student file (FileStorage)
        :return: all the students from the file (Pandas DataFrame)
        """
        ext = Validators.check_ext(value.filename, self._supported_student_files_ext)
        if not ext:
            raise ValueError(RestErrors.INVALID_STUDENTS_FILE)
        students_df = create_students_df(ext, value.stream)
        if students_df.shape[0] > self._max_students_in_class:
            raise ValueError(RestErrors.TO_MANY_RECORDS)
        if students_df.empty:
            raise ValueError(RestErrors.INVALID_STUDENTS_FILE)
        return parser.parse_df(students_df)

    def chat_file(self, value):
        """
        The function will make sure the chat file has the right extenstion
        :param value: the chat file (FileStorage)
        :return: The chat as dataframe (Pandas Dataframe)
        """
        if not Validators.check_ext(value.filename, self._supported_chat_file_ext):
            raise ValueError(RestErrors.INVALID_CHAT_FILE)
        chat_file = value.stream.read().decode("utf-8").split("\n") #TODO: check this in test
        chat_df = create_chat_df(chat_file)
        if chat_df.empty:
            raise ValueError(RestErrors.INVALID_CHAT_FILE)
        return chat_df

    @staticmethod
    def check_ext(file_name, extensions):
        """
        The function will check if the filename is one of the following extensions types
        :param file_name: the name of the file (str)
        :param extensions: list of extension to check (list)
        :return: the extension of the file name or None if don't exists (str
        """
        file_name = file_name.replace('"', "")  # Because of weird quotes postman adds to the filename
        for ext in extensions:
            if file_name.endswith(ext):
                return ext

    @staticmethod
    def any_of_chars_match(chars, string):
        """
        The function will check if any of the chars in one string is in the second string
        :param chars: list of chars to check (iterator of chars)
        :param string: string to check in (str)
        :return: the answer to the boolean question (bool)
        """
        return any([c in string for c in chars])


