from Server.config import ParseConfig
from Server.classrooms.loading_classroom_file import ParseClassFile


parser = ParseClassFile.from_object(ParseConfig)