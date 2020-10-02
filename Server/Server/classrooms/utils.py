import re
from datetime import datetime
import pandas as pd

def create_chat_df(chat_file):

    regex_pattern = re.compile(r"(^\d{2}.\d{2}.\d{2})\s+From\s\s([\s\S]+)\s:\s([\s\S]+)")
    chat_content = [re.search(regex_pattern, line).groups() for line in chat_file if re.match(regex_pattern, line)]

    chat_df = pd.DataFrame(chat_content, columns=["time", "zoom_name", "message"])
    chat_df['message'] = chat_df['message'].str[:-1].astype(str)
    chat_df["time"] = chat_df["time"].apply(lambda string: datetime.strptime(string, "%H:%M:%S"))

    return chat_df


def create_students_df(file_name, file_data):

    if file_name.endswith(".csv"):
        df_students = pd.read_csv(file_data)
    elif file_name.endswith(".xlsx"):
        df_students = pd.read_excel(file_data)
    else:
        df_students = pd.read_html(file_data, header=1)[0]

    return df_students