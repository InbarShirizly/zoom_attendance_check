import pandas as pd
import numpy as np
import re


class ParseClassFile:

    def __init__(self, file_cols_dict, mashov_cols, gender_dict):
        self._file_cols_dict = file_cols_dict
        self._mashov_cols = mashov_cols
        self._gender_dict = gender_dict

    @classmethod
    def from_object(cls, config):
        return cls(
            config.FILE_COLS_DICT,
            config.MASHOV_COLS,
            config.GENDER_DICT
        )


    def parse_df(self, df_students):
        relevant_cols = [col for col in df_students.columns if not col.startswith("Unnamed")]
        current_excel_dict = {}

        for col in relevant_cols:
            for key, col_options in self._file_cols_dict.items():
                if col in col_options:
                    current_excel_dict[key] = df_students[col]

        if len(current_excel_dict) == 0 and len(relevant_cols) <= 1:
            header_index = df_students.notnull().sum(axis=1).argmax()
            df_students = pd.DataFrame(df_students.values[header_index + 1:-2], columns=df_students.iloc[header_index])
            df_students.dropna(axis=0, how='all', inplace=True)
            df_students.dropna(axis=1, how='all', inplace=True)
            df_students.rename(columns={np.nan: 'name', "פרטי תלמיד": 'name', "כיתה": "org_class"}, inplace=True)
            df_students = df_students.loc[:, self._mashov_cols]

            mashov_name_pattern = re.compile(r"([\u0590-\u05fe ]+)([(\u0590-\u05fe)]+)")
            df_name_gender = df_students['name'].str.extract(mashov_name_pattern, expand=False)
            df_students['gender'] = df_name_gender[1].str.extract("\(([\u0590-\u05fe ])\)")
            df_students['gender'] = df_students['gender'].apply(self.gender_assign, gender_dict=self._gender_dict)
            df_students['name'] = df_name_gender[0]

        else:
            df_students = pd.DataFrame(current_excel_dict)

        for col in self._file_cols_dict.keys():
            try:
                df_students[col] = df_students[col]
            except KeyError:
                df_students[col] = pd.Series([np.nan] * df_students.shape[0])

        final_df = df_students[list(self._file_cols_dict.keys())]

        return final_df.reset_index().drop(columns="index")

    @staticmethod
    def gender_assign(string, gender_dict):
        for key, vals in gender_dict.items():
            if string in vals:
                return key
        return ""