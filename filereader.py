from typing import Type

from xml.sax import make_parser
from xml.sax.xmlreader import XMLReader
from zipfile import ZipFile
from xml_handlers import AbstractXmlHandler, SharedStringHandler


class FileReader:
    __string_handler: SharedStringHandler
    __parser: XMLReader
    __file_name: str
    data_handler: AbstractXmlHandler

    def __init__(self, file_name: str, data_handler: Type[AbstractXmlHandler], min_row: int = 1,):
        self.__file_name = file_name
        self.__parser = make_parser()
        self.__string_handler = SharedStringHandler()
        self.data_handler = data_handler(min_row=min_row)

    def __read_shared_string_file(self):
        zf = ZipFile(self.__file_name)
        return zf.open('xl/sharedStrings.xml')

    def __read_table_data_file(self):
        zf = ZipFile(self.__file_name)
        return zf.open('xl/worksheets/sheet1.xml')

    def __read_shared_string(self):
        self.__parser.setContentHandler(self.__string_handler)
        self.__parser.parse(self.__read_shared_string_file())

    def __read_table_data(self):
        self.__parser.setContentHandler(self.data_handler)
        self.data_handler.strings_mapping = self.__string_handler.strings_mapping
        self.__parser.parse(self.__read_table_data_file())

    def parse_data(self):
        self.__read_shared_string()
        self.__read_table_data()

    def read(self):
        self.parse_data()
