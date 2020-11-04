import pandas as pd
import numpy as np
import re
import json
from server.config import RestErrors


class ParseClassFile:
    """
    parse the excel/csv file uploaded to classroom data to insert to the database.
    supports regular files and "Mashov" format.
    """

    def __init__(self, file_cols_dict, mashov_cols, gender_dict, delete_rows_contain, unique_columns_restriction):
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
        self._unique_columns_restriction = unique_columns_restriction

    @classmethod
    def from_object(cls, config):
        return cls(
            config.FILE_COLS_DICT,
            config.MASHOV_COLS,
            config.GENDER_DICT,
            config.DELETE_ROWS_CONTAIN,
            config.UNIQUE_COLUMNS_RESTRICTION
        )

    def parse_df(self, df_students):
        """
        parsing the raw df from the file. parse different if mashov file, add all the columns that wasn't in the
        file but are part of the database. assigns gender for the relevant column. makes sure filter columns are unique
        and add country name and code as "public" unique data for each student
        :param df_students: given df
        :return: df parsed ready to load to db
        """
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
        final_df['gender'] = final_df['gender'].apply(self.gender_assign)  # assigning gender using the class func
        final_df = self.add_country_and_code_to_students(final_df)
        self.check_filter_columns_unique(final_df)  # check that all values in filters columns are unique
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
                if re.search(rf"\b{'|'.join(col_options)}(e)?(s)?\b", col):
                    current_excel_dict[key] = df_students[col]
                    break
        return pd.DataFrame(current_excel_dict)

    def check_filter_columns_unique(self, df_students):
        """
        check that the column that are filters (name, id, phone) have only unique value - if there is non unique
        column it will raise "INVALID_STUDENTS_FILE"
        :param df_students: df of the students
        :return: True or False
        """
        for col in df_students.columns:
            col_not_nans = df_students[col].notna().any() # boolean to check columns is not only nan
            if_filter_col = col in self._unique_columns_restriction # check that columns is part of the restricted ones
            if (not df_students[col].is_unique) and col_not_nans and if_filter_col:
                raise ValueError(RestErrors.INVALID_STUDENTS_FILE)


    def gender_assign(self, string):
        """
        assign gender to student from the string defining the gender (use the gender dict)
        :param string: student gender raw data from the loaded file
        :return: correct gender (bool) - or Nan (if there is not input)
        """
        for key, values in self._gender_dict.items():
            if string in values:
                return key
        return np.nan
    
    @staticmethod
    def add_country_and_code_to_students(df_students):
        """
        add random country and country code to each student
        :param df_students: df of the students
        :return: df enriched by country and code
        """
        with open(r"server\parsing\countries.json") as f:
            countries_json = json.load(f)
        countries_df = pd.DataFrame(countries_json).sample(len(df_students)).reset_index().drop(columns="index")
        countries_df.rename(columns={"name": "country", "code": "country_code"}, inplace=True)
        return pd.concat([df_students, countries_df], axis=1)
        
        