import pandas as pd
from sqlalchemy import create_engine
import os
import numpy as np
import re

STUDENT_FILES_FOLDER = './student_csv_examples'
EXCEL_PATH = ["דוגמה לרשימת תלמידים.xlsx", "רשימת תלמידים.xlsx", "רשימה שמית לקבוצה מתמטיקה 5 יב1 - יב4 פטרושקה רועי [185] (2).xls"]

SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

EXCEL_COLS = {
            "Name": ["שם התלמיד", "תלמידים", "שמות", "שם", "סטודנט"],
            "ID": ["תעודת זהות", "ת.ז.", "ת.ז", "תז"],
            "Phone": ["טלפון", "מספר טלפון", "מס טלפון"],
            "Gender": ["מין"],
            "org_class": ["כיתה"]
            }

MASHOW_COLS = ["Name", "org_class"]
gender_dict = {1: ["זכר", "ז", "(ז)"], 0: ["נקבה", "נ", "(נ)"]}
mashov_name_pattern = re.compile(r"([\u0590-\u05fe ]+)([(\u0590-\u05fe)]+)")


def gender_assign(string, gender_dict):
    for key, vals in gender_dict.items():
        if string in vals:
            return key
    return ""


def parse_excel(file_path):
    if file_path.endswith(".csv"):
        df_students = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df_students = pd.read_excel(file_path)
    else:
        df_students = pd.read_html(file_path, header=1)[0]

    relevant_cols = [col for col in df_students.columns if not col.startswith("Unnamed")]
    current_excel_dict = {}

    for col in relevant_cols:
        for key, col_options in EXCEL_COLS.items():
            if col in col_options:
                current_excel_dict[key] = df_students[col]

    if len(current_excel_dict) == 0 and len(relevant_cols) <= 1:
        print("Mashov file")
        header_index = df_students.notnull().sum(axis=1).argmax()
        df_students = pd.DataFrame(df_students.values[header_index + 1:-2], columns=df_students.iloc[header_index])
        df_students.dropna(axis=0, how='all', inplace=True)
        df_students.dropna(axis=1, how='all', inplace=True)
        df_students.rename(columns={np.nan: 'Name', "פרטי תלמיד": 'Name', "כיתה": "org_class"}, inplace=True)
        df_students = df_students.loc[:, MASHOW_COLS]

        df_name_gender = df_students.Name.str.extract(mashov_name_pattern, expand=False)
        df_students['Gender'] = df_name_gender[1].str.extract("\(([\u0590-\u05fe ])\)")
        df_students['Gender'] = df_students['Gender'].apply(gender_assign, gender_dict=gender_dict)
        df_students['Name'] = df_name_gender[0]

    else:
        df_students = pd.DataFrame(current_excel_dict)

    for col in EXCEL_COLS.keys():
        try:
            df_students[col] = df_students[col]
        except KeyError:
            df_students[col] = pd.Series([np.nan] * df_students.shape[0])

    return df_students[list(EXCEL_COLS.keys())]


if __name__ == '__main__':
    for e_path in EXCEL_PATH:
        student_file_path = os.path.join(STUDENT_FILES_FOLDER, e_path)
        df_students = parse_excel(student_file_path)
        print(df_students)

        df_students.to_sql('Students', con=engine, if_exists="append", index=False)

    student_sql = engine.execute("SELECT * FROM Students").fetchall()
    for student in student_sql:
        print(student)
