from typing import List

from lxml.etree import parse

from file_readers.abstract_file_reader import AbstractFileReader


class LXMLFileReader(AbstractFileReader):

    def __init__(self, file_name: str, data_handler, min_row: int = 1):
        super().__init__(file_name)
        self.__shared_strings: List[str]
        self.__table_data: List[str]
        self.__data_handler_class = data_handler
        self.__min_row = min_row
        self.data_handler = None

    def _read_shared_string(self):
        tree = parse(self._read_shared_string_file())
        root = tree.getroot()
        self.__shared_strings = list(map(lambda x: x.text, root.findall('.//{*}t')))

    def _read_table_data(self):
        self.__init_data_handler()
        self.data_handler.parse_data()

    def iter_rows(self):
        return self.data_handler.iter_rows()

    def __init_data_handler(self):
        self.data_handler = self.__data_handler_class(
            self._read_table_data_file(),
            self.__shared_strings,
            self.__min_row,
        )
