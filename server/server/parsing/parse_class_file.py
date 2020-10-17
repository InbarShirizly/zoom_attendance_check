import pandas as pd
import numpy as np
import re
from server.config import RestErrors


class ParseClassFile:
    """
    parse the excel/csv file uploaded to classroom data to insert to the database.
    supports regular files and "Mashov" format.
    """

    def __init__(self, file_cols_dict, mashov_cols, gender_dict, delete_rows_contain):
        """
        receives configurations from "from object" which is initiated in the config module
        :param file_cols_dict: columns name in the DB (keys)
                               and option names that could appear in the loading file (values) - dict
        :param mashov_cols: specific column names in DB that will be filled from Mashov file format (list of str)
        :param gender_dict: transformation dict for optional gender format in loaded file
                            (dict: key-bool (Male==1, Female==0), values= list of optional strings)
        :param delete_rows_contain: string that might appear in rows in the loaded file that should be deleted (list of str)
        """
        self._file_cols_dict = file_cols_dict
        self._mashov_cols = mashov_cols
        self._gender_dict = gender_dict
        self._delete_rows_contain = delete_rows_contain
        # TODO: should add here the filter modes - which are the columns which must be unique
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
        """
        check if the loaded file have a "Mashov" format - checking the format if the columns of the names
        example of the format: "1. אבי גילי סימ (נ)".
        If the file is mashov, change column name accordingly
        :param df_students: loaded student list file already cleaned
        :return: boolean - True if it is a mashov file (and change the "global" df meanwhile)
        """
        df_students.dropna(axis=0, how="all", inplace=True)
        df_students.dropna(axis=1, how="all", inplace=True)

        for col in df_students.columns:
            if df_students[col].astype(str).str.match(r"(\d+.)([\u0590-\u05fe ]+)([(\u0590-\u05fe)]+)").any():
                df_students.rename(columns={col: "name"}, inplace=True)
                return True
        return False

    def mashov_file(self, df_students):
        """
        parse the Mashov file format
        :param df_students: df of the cleaned mashov file (df)
        :return: data frame with relevant data to insert to the DB (df)
        """
        df_t = df_students.T
        cols_to_drop = []
        for col in df_t.columns:
            # drop all "columns" (rows that transposed) the contain any of the "delete rows" strings
            if df_t[col].str.contains('|'.join(self._delete_rows_contain)).any():
                cols_to_drop.append(col)
        df_students = df_t.drop(columns=cols_to_drop).T

        df_students.rename(columns={"תז": 'id_number', "כיתה": "org_class"}, inplace=True)
        try:
            # slice only the columns of data that is relevant to insert to the DB
            df_students = df_students.loc[:, self._mashov_cols]
        except KeyError:
            # if the file don't contain one of the columns - raises ValueError
            raise ValueError(RestErrors.INVALID_STUDENTS_FILE)

        # extracing the name column from mashov pattern, dealing with gender
        mashov_name_pattern = re.compile(r"([\u0590-\u05fe ]+)([(\u0590-\u05fe)]+)")
        df_name_gender = df_students['name'].str.extract(mashov_name_pattern, expand=False)
        df_students['gender'] = df_name_gender[1].str.extract("\(([\u0590-\u05fe ])\)")
        df_students['gender'] = df_students['gender'].apply(self.gender_assign, gender_dict=self._gender_dict)
        df_students['name'] = df_name_gender[0]
        return df_students


    def classic_file(self, df_students):
        """
        parse "classic" files - get all columns with relevant data and create df accordingly
        :param df_students: df of the cleaned "classic" file (df)
        :return: data frame with relevant data to insert to the DB (df)
        """
        relevant_cols = [col for col in df_students.columns if not col.startswith("Unnamed")]
        current_excel_dict = {}
        for col in relevant_cols:
            for key, col_options in self._file_cols_dict.items():
                if col in col_options:
                    current_excel_dict[key] = df_students[col]
        return pd.DataFrame(current_excel_dict)

    def check_filter_columns_unique(self): # TODO: create this function
        # try:
        #     # slice only the columns of data that is relevant to insert to the DB
        #     df_students = df_students.loc[:, self._mashov_cols]
        # except KeyError:
        #     # if the file don't contain one of the columns - raises ValueError
        #     raise ValueError(RestErrors.INVALID_STUDENTS_FILE)
        pass

    @staticmethod
    def gender_assign(string, gender_dict):  # TODO: deal with cases of Unknown gender
        """
        assign gender to student from the string defining the gender (use the gender dict)
        :param string: student gender raw data fron the loaded file
        :param gender_dict: transformation dict for optional gender format in loaded file
        :return: correct gender (bool)
        """
        for key, values in gender_dict.items():
            if string in values:
                return key
        return ""


