from abc import ABC, abstractmethod
from typing import List

from lxml.etree import parse

from schemas.table_enums import XLSTagTypes, XLSRowTagNames


class LXMLAbstractHandler(ABC):

    NAMESPACE_IGNORE_PATTERN = ".//{*}"

    def __init__(self, table_file: str, shared_strings: List[str], min_row: int = 1):
        self._min_row = min_row
        self._shared_strings = shared_strings
        self._table_data = []
        self._table_file = table_file

    def parse_data(self):
        tree = parse(self._table_file)
        root = tree.getroot()
        for row in root.findall(self._row_search_pattern):
            row_number = int(row.attrib.get(XLSRowTagNames.ROW_NUMBER))
            if row_number < self._min_row:
                continue
            self._parse_row_child(row=row, number=row_number)

    @abstractmethod
    def _map_sheet(self, cell, value):
        raise NotImplementedError()

    @abstractmethod
    def _parse_row_child(self, row, number):
        raise NotImplementedError()

    def iter_rows(self):
        for row in self._table_data[1:]:
            yield row

    @property
    def _row_search_pattern(self):
        return f'{self.NAMESPACE_IGNORE_PATTERN}{XLSTagTypes.ROW}'

    @property
    def _cell_search_pattern(self):
        return f'{self.NAMESPACE_IGNORE_PATTERN}{XLSTagTypes.CELL}'

    @property
    def _value_search_pattern(self):
        return f'{self.NAMESPACE_IGNORE_PATTERN}{XLSTagTypes.VALUE}'
