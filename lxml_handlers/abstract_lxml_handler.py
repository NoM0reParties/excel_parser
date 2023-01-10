from abc import ABC, abstractmethod
from functools import cached_property
from typing import List

from lxml.etree import parse

from schemas.table_enums import XLSTagTypes, XLSRowTagNames, XLSTableValueType


class LXMLAbstractHandler(ABC):

    VALUE_FROM_MAPPING = {
        XLSTableValueType.STRING: XLSTagTypes.VALUE,
        XLSTableValueType.NUMBER: XLSTagTypes.VALUE,
        XLSTableValueType.INLINE_STRING: XLSTagTypes.INLINE_STRING,
        XLSTableValueType.UNKNOWN: XLSTagTypes.FORMULA,
    }

    NAMESPACE_IGNORE_PATTERN = ".//{*}"

    def __init__(self, table_file: str, shared_strings: List[str], min_row: int = 1):
        self._min_row = min_row
        self._shared_strings = shared_strings
        self._table_data = []
        self._table_file = table_file
        self._value_from: XLSTagTypes = XLSTagTypes.UNKNOWN
        self._data_type: XLSTableValueType = XLSTableValueType.UNKNOWN

    def _set_value_from(self):
        if self._data_type:
            self._value_from = self.VALUE_FROM_MAPPING[self._data_type]

    def parse_data(self):
        tree = parse(self._table_file)
        root = tree.getroot()
        self._table_data = list(
            map(
                self._parse_row_child,
                filter(
                    self.__min_row_filter,
                    root.findall(self._row_search_pattern)
                )
            )
        )

    def __min_row_filter(self, row) -> bool:
        row_number = int(row.attrib.get(XLSRowTagNames.ROW_NUMBER))
        if row_number < self._min_row:
            return False
        return True

    @abstractmethod
    def _map_sheet(self, cell):
        raise NotImplementedError()

    @abstractmethod
    def _parse_row_child(self, row):
        raise NotImplementedError()

    @cached_property
    def _row_search_pattern(self):
        return f'{self.NAMESPACE_IGNORE_PATTERN}{XLSTagTypes.ROW}'

    @cached_property
    def _cell_search_pattern(self):
        return f'{self.NAMESPACE_IGNORE_PATTERN}{XLSTagTypes.CELL}'

    @property
    def _value_search_pattern(self):
        return f'{self.NAMESPACE_IGNORE_PATTERN}{self._value_from}'
