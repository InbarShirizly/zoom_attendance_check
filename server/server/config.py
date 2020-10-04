import string


class FlaskConfig:
    SECRET_KEY = 'TEMP_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


class ParseConfig:
    FILE_COLS_DICT = {
        "name": ["שם התלמיד", "תלמידים", "שמות", "שם", "סטודנט"],
        "id_number": ["תעודת זהות", "ת.ז.", "ת.ז", "תז"],
        "phone": ["טלפון", "מספר טלפון", "מס טלפון"],
        "gender": ["מין"],
        "org_class": ["כיתה"]
    }
    MASHOV_COLS = ["name", "org_class"]
    GENDER_DICT = {1: ["זכר", "ז", "(ז)"], 0: ["נקבה", "נ", "(נ)"]}


class ValidatorsConfig:
    INVALID_USERNAME_CHARS = '!='
    MIN_PASSWORD_LEN = 4
    REQUIRED_PASSWORD_CHARS = [string.ascii_lowercase, string.ascii_uppercase, string.digits]

class RestErrors:
    INVALID_ROUTE = "Route does't exist"
    INVALID_CLASS = "Invalid class id"
    INVALID_REPORT = "Invalid report id"
    INVALID_STATUS = "Invalid status id"
    USERNAME_TAKEN = "Username already taken"
    EMAIL_TAKEN = "Email already taken"
    ILLEGAL_USERNAME_CHARS = f'Username can\'t contain the following characthers: "{ValidatorsConfig.INVALID_USERNAME_CHARS}"' 
    PASSWORD_TO_SHORT = f'Password to short, must be at least {ValidatorsConfig.MIN_PASSWORD_LEN} chars long'
    PASSWORD_MUST_CONTAIN = 'Password must contain at least one lower case letter one upper case letter and a digit'