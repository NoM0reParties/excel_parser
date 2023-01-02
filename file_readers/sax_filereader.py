from typing import Type

from xml.sax import make_parser

from file_readers.abstract_file_reader import AbstractFileReader
from sax_handlers import AbstractXmlHandler, SharedStringHandler


class SaxFileReader(AbstractFileReader):

    def __init__(self, file_name: str, data_handler: Type[AbstractXmlHandler], min_row: int = 1):
        super().__init__(file_name)
        self.__parser = make_parser()
        self.__string_handler = SharedStringHandler()
        self.data_handler = data_handler(min_row=min_row)

    def _read_shared_string(self):
        self.__parser.setContentHandler(self.__string_handler)
        self.__parser.parse(self._read_shared_string_file())

    def _read_table_data(self):
        self.__parser.setContentHandler(self.data_handler)
        self.data_handler.strings_mapping = self.__string_handler.strings_mapping
        self.__parser.parse(self._read_table_data_file())

    def iter_rows(self):
        return self.data_handler.iter_rows()
