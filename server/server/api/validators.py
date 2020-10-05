from server import db, bcrypt
from server.models.orm import TeacherModel
from server.config import RestErrors
import email_validator
from datetime import datetime
import os
from werkzeug.datastructures import FileStorage


# The class is responsible for validating diffrent inputs to the API
class Validators:
    def __init__(self, date_format, supported_chat_file_ext, supported_student_files_ext, invalid_username_chars="", min_password_len=0, required_password_chars=[]):
        self._date_format = date_format
        self._supported_chat_file_ext = supported_chat_file_ext
        self._supported_student_files_ext = supported_student_files_ext
        self._invalid_username_chars = invalid_username_chars
        self._min_password_len = min_password_len
        self._required_password_chars = required_password_chars

    @classmethod
    def from_object(cls, config):
        """
        The function will init an instance from config object
        """
        return cls(
            config.DATE_FORMAT,
            config.CHAT_FILE_EXT,
            config.STUDENTS_FILE_EXT,
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
        :param value: the input data (str)
        :reutrn value: the date (datetime)
        """
        return datetime.strptime(value, self._date_format)
    
    def students_file(self, value):
        """
        The function will make sure the student file has the right extenstion
        :param value: the student file (FileStorage)
        :return: the student file (FileStorage)
        """
        if not Validators.check_ext(value.filename, self._supported_student_files_ext):
            raise ValueError(RestErrors.INVALID_STUDENTS_FILE)
        return value

    def chat_file(self, value):
        """
        The function will make sure the chat file has the right extenstion
        :param value: the chat file (FileStorage)
        :return: the chat file (FileStorage)
        """
        if not Validators.check_ext(value.filename, self._supported_chat_file_ext):
            raise ValueError(RestErrors.INVALID_CHAT_FILE)
        return value

    @staticmethod
    def check_ext(file_name, extenstions):
        """
        The function will check if the filename is one of the following extentions types
        :param file_name: the name of the file (str)
        :extenstions: list of extension to check (list)
        :return: the answer to the boolean question (bool)
        """
        file_name = file_name.replace('"', "") # Becasue of wierd quotes postman adds to the filename
        return any([file_name.endswith(ext) for ext in extenstions])

    @staticmethod
    def any_of_chars_match(chars, string):
        """
        The function will check if any of the chars in one string is in the second string
        :param chars: list of chars to check (iterator of chars)
        :param string: string to check in (str)
        :return: the answer to the boolean question (bool)
        """
        return any([c in string for c in chars])
