from server import db, bcrypt
from server.models.orm import TeacherModel
from server.config import RestErrors
import email_validator
from datetime import datetime

# The class is responsible for validating diffrent inputs to the API
class Validators:
    def __init__(self, date_format, invalid_username_chars="", min_password_len=0, required_password_chars=[]):
        self._date_format = date_format
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
        if TeacherModel.query.filter_by(email=value).first():
            raise ValueError(RestErrors.EMAIL_TAKEN)
        return email_validator.validate_email(value).email

    def password(self, value):
        """
        The function will check if the password is valid (Containing at least one of each required char groups, longer than the min length)
        :param value: the password to check (str)
        :return: hashed password to store in the db (str)
        """
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
 

    @staticmethod
    def any_of_chars_match(chars, string):
        return any([c in string for c in chars])
