from filereader import FileReader
from schemas import ExtractModes
from xml_handlers import RawTableDataHandler, TableDataHandler


class DataExtractor:

    def __init__(
            self,
            file_name: str,
            mode: ExtractModes = ExtractModes.SIMPLE,
            min_row: int = 1,
            engine: ... = ...
    ):
        self.__mode = mode
        self.__engine = engine
        self.__file_reader = FileReader(
            file_name=file_name,
            data_handler=self.__get_handler_by_mode,
            min_row=min_row,
        )
        self.__data_read = False

    def read_data(self):
        if not self.__data_read:
            self.__file_reader.read()
        self.__data_read = True

    def iter_rows(self):
        self.read_data()
        return self.__file_reader.data_handler.iter_rows()

    @property
    def __get_handler_by_mode(self):
        if self.__mode == ExtractModes.SIMPLE:
            return RawTableDataHandler
        return TableDataHandler
