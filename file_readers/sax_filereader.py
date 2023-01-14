from typing import Type, Optional

from xml.sax import make_parser

from file_readers.abstract_file_reader import AbstractFileReader
from sax_handlers import AbstractXmlHandler, SharedStringHandler, WorkbookHandler


class SaxFileReader(AbstractFileReader):

    def __init__(
            self,
            file_name: str,
            data_handler: Type[AbstractXmlHandler],
            min_row: int = 1,
            sheet_name: Optional[str] = None
    ):
        super().__init__(file_name, sheet_name)
        self.__parser = make_parser()
        self.__string_handler = SharedStringHandler()
        self.__workbook_handler = WorkbookHandler()
        self.data_handler = data_handler(min_row=min_row)

    def _read_shared_string(self):
        strings_file = self._read_shared_string_file()
        if strings_file is None:
            return
        self.__parser.setContentHandler(self.__string_handler)
        self.__parser.parse(strings_file)

    def _read_table_data(self):
        self.__parser.setContentHandler(self.data_handler)
        self.data_handler.strings_mapping = self.__string_handler.strings_mapping
        self.__parser.parse(self._read_table_data_file())

    def iter_rows(self):
        return self.data_handler.iter_rows()

    def _find_xml_file_by_sheet_name(self):
        if self._sheet_name is None:
            return
        self.__make_sheets_mapping()
        print(self._sheet_name, self.__worksheet_mapping)
        self._table_data_xml_file_id = self.__worksheet_mapping.get(self._sheet_name)

    def __make_sheets_mapping(self):
        self.__parser.setContentHandler(self.__workbook_handler)
        self.__parser.parse(f"{self.MAIN_FOLDER}/workbook.xml")
        self.__worksheet_mapping = self.__workbook_handler.file_name_to_id_mapping

