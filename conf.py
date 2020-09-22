import re
import numpy as np


EXCEL_COLS = {"Name": "שם התלמיד",
              "ID": "תעודת זהות",
              "Phone": "טלפון"}


# constants
CHAT_PATTERN = re.compile(r"(^\d{2}.\d{2}.\d{2})\s+From\s\s([\s\S]+)\s:\s([\s\S]+)")


