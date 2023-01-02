from abc import ABC, abstractmethod
from zipfile import ZipFile


class AbstractFileReader(ABC):

    def __init__(self, file_name: str):
        self._file_name = file_name

    def _read_shared_string_file(self):
        zf = ZipFile(self._file_name)
        return zf.open('xl/sharedStrings.xml')

    def _read_table_data_file(self):  # TODO learn how to handle different sheetnames
        zf = ZipFile(self._file_name)
        return zf.open('xl/worksheets/sheet1.xml')

    @abstractmethod
    def _read_shared_string(self):
        raise NotImplementedError()

    @abstractmethod
    def _read_table_data(self):
        raise NotImplementedError()

    @abstractmethod
    def iter_rows(self):
        raise NotImplementedError()

    def parse_data(self):
        self._read_shared_string()
        self._read_table_data()

    def read(self):
        self.parse_data()
