from abc import ABC, abstractmethod
from typing import Optional
from zipfile import ZipFile


class AbstractFileReader(ABC):

    MAIN_FOLDER = "xl"
    WORKSHEET_FOLDER = "worksheets"
    WORKSHEET_NAME_TEMPLATE = "sheet{}.xml"

    def __init__(self, file_name: str, sheet_name: Optional[str] = None):
        self._file_name = file_name
        self._sheet_name = sheet_name
        self._table_data_xml_file_id = 1

    def _read_shared_string_file(self):
        zf = ZipFile(self._file_name)
        try:
            return zf.open(f'{self.MAIN_FOLDER}/sharedStrings.xml')
        except KeyError:
            return

    def _read_table_data_file(self):
        zf = ZipFile(self._file_name)
        worksheet_name = self.WORKSHEET_NAME_TEMPLATE.format(self._table_data_xml_file_id)
        return zf.open(f'{self.MAIN_FOLDER}/{self.WORKSHEET_FOLDER}/{worksheet_name}')

    @abstractmethod
    def _read_shared_string(self):
        raise NotImplementedError()

    @abstractmethod
    def _find_xml_file_by_sheet_name(self):
        raise NotImplementedError()

    @abstractmethod
    def _read_table_data(self):
        raise NotImplementedError()

    @abstractmethod
    def iter_rows(self):
        raise NotImplementedError()

    def parse_data(self):
        self._find_xml_file_by_sheet_name()
        self._read_shared_string()
        self._read_table_data()

    def read(self):
        self.parse_data()
