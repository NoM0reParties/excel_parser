from typing import List, Dict, Optional

from lxml.etree import parse

from file_readers.abstract_file_reader import AbstractFileReader


class LXMLFileReader(AbstractFileReader):

    def __init__(self, file_name: str, data_handler, min_row: int = 1, sheet_name: Optional[str] = None):
        super().__init__(file_name, sheet_name)
        self.__shared_strings: List[str]
        self.__table_data: List[str]
        self.__data_handler_class = data_handler
        self.__min_row = min_row
        self.data_handler = None
        self.__worksheet_mapping: Dict[str, str] = {}

    def _read_shared_string(self):
        strings_file = self._read_shared_string_file()
        if strings_file is None:
            self.__shared_strings = None
            return
        tree = parse(strings_file)
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

    def _find_xml_file_by_sheet_name(self):
        if self._sheet_name is None:
            return
        self.__make_sheets_mapping()
        print(self._sheet_name, self.__worksheet_mapping)
        self._table_data_xml_file_id = self.__worksheet_mapping.get(self._sheet_name)

    def __make_sheets_mapping(self):
        tree = parse(f"{self.MAIN_FOLDER}/workbook.xml")
        root = tree.getroot()
        self.__worksheet_mapping = {row.get("name"): row.get("sheetId") for row in root.findall('.//{*}sheet')}
