from Server.config import ParseConfig
from Server.utils.loading_classroom_file import ParseClassFile
from collections import namedtuple


parser = ParseClassFile.from_object(ParseConfig)

AttendanceMetaData = namedtuple('meta_data', ['filter_modes', 'time_delta', 'start_sentence', 'not_included_zoom_users'])
