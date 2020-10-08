import pandas as pd
import numpy as np
import re
from server.config import RestErrors


class ParseClassFile:

    def __init__(self, file_cols_dict, mashov_cols, gender_dict, delete_rows_contain):
        self._file_cols_dict = file_cols_dict
        self._mashov_cols = mashov_cols
        self._gender_dict = gender_dict
        self._delete_rows_contain = delete_rows_contain

    @classmethod
    def from_object(cls, config):
        return cls(
            config.FILE_COLS_DICT,
            config.MASHOV_COLS,
            config.GENDER_DICT,
            config.DELETE_ROWS_CONTAIN
        )

    def parse_df(self, df_students):
        if ParseClassFile.check_if_mashov_file(df_students):
            df_students = self.mashov_file(df_students)
        else:
            df_students = self.classic_file(df_students)

        for col in self._file_cols_dict.keys():
            try:
                df_students[col] = df_students[col]
            except KeyError:
                df_students[col] = pd.Series([np.nan] * df_students.shape[0])

        final_df = df_students[list(self._file_cols_dict.keys())]

        return final_df.reset_index().drop(columns="index")


    @staticmethod
    def check_if_mashov_file(df_students):
        df_students.dropna(axis=0, how="all", inplace=True)
        df_students.dropna(axis=1, how="all", inplace=True)

        for col in df_students.columns:
            if df_students[col].astype(str).str.match(r"(\d+.)([\u0590-\u05fe ]+)([(\u0590-\u05fe)]+)").any():
                df_students.rename(columns={col: "name"}, inplace=True)
                return True
        return False

    def mashov_file(self, df_students):
        df_t = df_students.T
        cols_to_drop = []
        for col in df_t.columns:
            if df_t[col].str.contains('|'.join(self._delete_rows_contain)).any():
                cols_to_drop.append(col)
        df_students = df_t.drop(columns=cols_to_drop).T

        df_students.rename(columns={"ת.ז.": 'id_number', "כיתה": "org_class"}, inplace=True)
        try:
            df_students = df_students.loc[:, self._mashov_cols]
        except KeyError:
            raise ValueError(RestErrors.INVALID_STUDENTS_FILE)

        mashov_name_pattern = re.compile(r"([\u0590-\u05fe ]+)([(\u0590-\u05fe)]+)")  #TODO: move regex to config
        df_name_gender = df_students['name'].str.extract(mashov_name_pattern, expand=False)
        df_students['gender'] = df_name_gender[1].str.extract("\(([\u0590-\u05fe ])\)")
        df_students['gender'] = df_students['gender'].apply(self.gender_assign, gender_dict=self._gender_dict)
        df_students['name'] = df_name_gender[0]
        return df_students

    def classic_file(self, df_students):
        relevant_cols = [col for col in df_students.columns if not col.startswith("Unnamed")]
        current_excel_dict = {}
        for col in relevant_cols:
            for key, col_options in self._file_cols_dict.items():
                if col in col_options:
                    current_excel_dict[key] = df_students[col]
        return pd.DataFrame(current_excel_dict)

    @staticmethod
    def gender_assign(string, gender_dict):
        for key, values in gender_dict.items():
            if string in values:
                return key
        return ""
