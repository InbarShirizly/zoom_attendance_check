from server import db, bcrypt
from server.models.orm import TeacherModel
from server.config import RestErrors
import email_validator


class Validators:
    def __init__(self, invalid_username_chars="", min_password_len=0, required_password_chars=[]):
        self._invalid_username_chars = invalid_username_chars
        self._min_password_len = min_password_len
        self._required_password_chars = required_password_chars

    def username(self, value):
        if TeacherModel.query.filter_by(username=value).first():
            raise ValueError(RestErrors.USERNAME_TAKEN)
        if Validators.any_of_chars_match(self._invalid_username_chars, value):
            raise ValueError(RestErrors.ILLEGAL_USERNAME_CHARS)
        return value

    def email(self, value):
        if TeacherModel.query.filter_by(email=value).first():
            raise ValueError(RestErrors.EMAIL_TAKEN)
        return email_validator.validate_email(value).email

    def password(self, value):
        if len(value) < self._min_password_len:
            raise ValueError(RestErrors.PASSWORD_TO_SHORT)
        for chars_list in self._required_password_chars:
            if not Validators.any_of_chars_match(chars_list, value):
                raise ValueError(RestErrors.PASSWORD_MUST_CONTAIN)
        return bcrypt.generate_password_hash(value).decode('utf-8')

    @staticmethod
    def any_of_chars_match(chars, string):
        return any([c in string for c in chars])
