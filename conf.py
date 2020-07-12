import re
import numpy as np


# variables to change
FILE_NAME = ".\chat files\meeting_saved_chat3.txt"
SENTENCE_START = "attendance check"
TIME_DELTA = np.timedelta64(6, 'm')  # time period
COLUMNS_NAMES = ["time", "users", "chat"]
WORDS_FOR_NOT_INCLUDED_PARTICIPATORS = ["ITC", "Tech", "Challenge"]


# constants
JSON_FILE_NAME = "zoom_names_to_full_names"
CHAT_PATTERN = re.compile(r"(^\d{2}.\d{2}.\d{2})\s+From\s\s([\s\S]+)\s:\s([\s\S]+)")
class_names = ['Andrey Bakhmat', 'Areej Eweida', 'Ariela Strimling',
               'Ariella Berger', 'Aviv Kadair', 'Dana Makov', 'Daniel Kagan', 'Hanna Hier',
               'Inbar Shirizly', 'Itamar Meimon', 'Jonathan Bitton', 'Kevin Daniels', 'Limor Nunu',
               'Lucas Gilbert Bensaid', 'May Lev Steinfeld', 'Michael Marcus', 'Michael Goncharov',
               'Nicolas Mai', 'Nir Barazida', 'Ori Kleinhauz', 'Ron Zehavi', 'Rozanna Royter',
               'Sebastian Kleiner', 'Serah Abensour', 'Sheryl Sitruk', 'Tal Toledano',
               'Tammuz Dubnov', 'Yuval Herman']


