import re
from datetime import datetime
import pandas as pd
import numpy as np


def create_chat_df(chat_file):
    """
    parse the raw chat file from zoom to a df. if a row is not in the "zoom row format" it will not be part of the df
    In this way, any text file that don't match zoom chat pattern will return empty data-frame
    :param chat_file: loaded chat file (TextIowrapper - file after "open" / "stream")
    :return: chat rows that passed the zoom parsing pattern (df)
    """

    regex_pattern = re.compile(r"(^\d{2}.\d{2}.\d{2})\s+From\s\s([\s\S]+)\s:\s([\s\S]+)")
    chat_content = [re.search(regex_pattern, line).groups() for line in chat_file if re.match(regex_pattern, line)]

    chat_df = pd.DataFrame(chat_content, columns=["time", "zoom_name", "message"])
    chat_df['message'] = chat_df['message'].str[:-1].astype(str)  # remove end of line (could be "/n" or "/t")
    chat_df["time"] = chat_df["time"].apply(lambda string: datetime.strptime(string, "%H:%M:%S"))
    return chat_df


def create_students_df(file_ext, file_data):
    """
    use pandas to create df of loaded file. check extension of the file to use the correct pandas "read" method
    supporting - "xls", "xlsx", "csv" - the validation for the ext happens in the validation class before this
    function runs.
    The dataframe cleans not relevant rows and columns using external function
    :param file_ext: extension of the current file (str)
    :param file_data: raw data of the loaded file
    :return: cleaned df of the students list (df)
    """
    if file_ext == ".csv":
        df_students = pd.read_csv(file_data, header=None)
    elif file_ext == ".xlsx":
        df_students = pd.read_excel(file_data, header=None)
    else:
        try:
            df_students = pd.read_html(file_data, header=1)[0]
        except ValueError:
            df_students = pd.ExcelFile(file_data).parse()
    clean_df = clean_student_df(df_students)
    return clean_df


def clean_student_df(df_students):
    """
    cleaning process over the student list data-frame.
    1. removes empty rows and columns
    2. drop columns that don't contain more then 3 unique values (at least title and 2 students)
    3. set the titles of the columns to be the df headers
    :param df_students: input df parsed from previous function (df)
    :return: cleaned df (df)
    """
    # # first drop al columns that are totally missing (for extreme cases)
    df_students.dropna(axis=0, how="all", inplace=True)
    df_students.dropna(axis=1, how="all", inplace=True)

    # drop columns with at least 20% missing values
    df_students.dropna(axis=1, thresh=len(df_students) * 0.2, inplace=True)
    df_students = pd.DataFrame(df_students.values[1:], columns=df_students.iloc[0])
    # clean columns names - rename to more generic form
    df_students.columns = [clean_string(col) if isinstance(col, str) else np.nan for col in df_students.columns]
    # drop column with the same name - keep the first
    df_students = df_students.loc[:, ~df_students.columns.duplicated()]   # drop column with the same name - keep the first
    return df_students


def clean_string(string):
    return re.sub(r"['\".\/\\]", "", string=string).lower().replace("_"," ").strip()


