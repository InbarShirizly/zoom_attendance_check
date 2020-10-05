class FlaskConfig:
    SECRET_KEY = 'TEMP_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


class ParseConfig:
    FILE_COLS_DICT = {
        "name": ["שם התלמיד", "תלמידים", "שמות", "שם", "סטודנט", "name", "student_name", "student"],
        "id_number": ["תעודת זהות", "ת.ז.", "ת.ז", "תז", "id", "number_id", "id_number"],
        "phone": ["טלפון", "מספר טלפון", "מס טלפון", "phone", "phone_number"],
        "gender": ["מין", "gender"],
        "org_class": ["כיתה", "org_class", "class"]
    }
    MASHOV_COLS = ["name", "org_class", "id_number"]
    GENDER_DICT = {1: ["זכר", "ז", "(ז)"], 0: ["נקבה", "נ", "(נ)"]}


class RestErrors:
    INVALID_ROUTE = "Route does't exist"
    INVALID_CLASS = "Invalid class id"
    INVALID_REPORT = "Invalid report id"
    INVALID_STATUS = "Invalid status id"
    USERNAME_TAKEN = "Username already taken"
    EMAIL_TAKEN = "Email already taken"