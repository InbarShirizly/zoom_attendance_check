from src.config import ParseConfig
from src.parsing.parse_class_file import ParseClassFile
from collections import namedtuple

# create parser instance
parser = ParseClassFile.from_object(ParseConfig)
# create namedtuple instance called "meta_data" - with variables that will be inserted to the Attendance class
AttendanceMetaData = namedtuple('meta_data', ['filter_modes', 'time_delta', 'start_sentence', 'zoom_names_to_ignore'])
