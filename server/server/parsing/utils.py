import re
from datetime import datetime
import pandas as pd

def create_chat_df(chat_file):

    regex_pattern = re.compile(r"(^\d{2}.\d{2}.\d{2})\s+From\s\s([\s\S]+)\s:\s([\s\S]+)")
    chat_content = [re.search(regex_pattern, line).groups() for line in chat_file if re.match(regex_pattern, line)]

    chat_df = pd.DataFrame(chat_content, columns=["time", "zoom_name", "message"])
    chat_df['message'] = chat_df['message'].str[:-1].astype(str)
    chat_df["time"] = chat_df["time"].apply(lambda string: datetime.strptime(string, "%H:%M:%S"))
    if chat_df.empty:
        raise ValueError("Entered file is empty")
    return chat_df


def create_students_df(file_name, file_data):
    if file_name.endswith(".csv"):
        df_students = pd.read_csv(file_data, header=None)
    elif file_name.endswith(".xlsx"):
        df_students = pd.read_excel(file_data, header=None)
    else:
        try:
            df_students = pd.read_html(file_data, header=1)[0]
        except ValueError:
            df_students = pd.ExcelFile(file_data).parse()

    clean_df = clean_student_df(df_students)

    if clean_df.shape[0] > 200:
        raise ValueError("Input file have to many records")  #TODO: pass amount of records as config
    if clean_df.empty:
        raise ValueError("Entered file is empty")
    return clean_df


def clean_student_df(df_students):
    # # first drop al columns that are totally missing (for extreme cases)
    df_students.dropna(axis=0, how="all", inplace=True)
    df_students.dropna(axis=1, how="all", inplace=True)

    # check for unique values in columns - must have at list 3 unique values (min of title and 2 students
    min_nunique_in_cols = max(df_students.nunique().median(), 3)
    filt_relevant_cols = df_students.nunique() >= min_nunique_in_cols
    df_students = df_students.loc[:, filt_relevant_cols]
    df_students = pd.DataFrame(df_students.values[1:], columns=df_students.iloc[0])
    return df_students


