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


class RestErrors:
    INVALID_ROUTE = "Route does't exist"
    INVALID_CLASS = "Invalid class id"
    INVALID_REPORT = "Invalid report id"
    INVALID_STATUS = "Invalid status id"
    USERNAME_TAKEN = "Username already taken"
    EMAIL_TAKEN = "Email already taken"