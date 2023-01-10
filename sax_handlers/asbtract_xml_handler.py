from abc import abstractmethod
from typing import Optional, List
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl

from schemas import XLSTableValueType, XLSTagTypes, XLSRowTagNames


class AbstractXmlHandler(ContentHandler):

    VALUE_FROM_MAPPING = {
        XLSTableValueType.STRING: XLSTagTypes.VALUE,
        XLSTableValueType.NUMBER: XLSTagTypes.VALUE,
        XLSTableValueType.INLINE_STRING: XLSTagTypes.INLINE_STRING,
        XLSTableValueType.UNKNOWN: XLSTagTypes.FORMULA,
    }

    def __init__(self, min_row: int = 1):
        super().__init__()
        self.row_number = 0
        self._current_el: Optional[str] = None
        self.strings_mapping: List[str] = []
        self._tag_content: str = ""
        self._data_type: XLSTableValueType = XLSTableValueType.UNKNOWN
        self._iter_count: int = 0
        self.__min_row = min_row
        self._value_from: XLSTagTypes = XLSTagTypes.UNKNOWN

    def startElement(self, name: str, attrs: AttributesImpl):
        self._tag_content = ""
        if name == XLSTagTypes.CELL:
            self._set_data_type(attrs=attrs)
        if name == XLSTagTypes.ROW:
            self.row_number = int(attrs.get(XLSRowTagNames.ROW_NUMBER))
            self._set_current_row()

    def characters(self, content):
        self._tag_content += content

    def endElement(self, name: str):
        if name == self._value_from:
            self._set_cell_value()
        elif name == XLSTagTypes.ROW:
            if self.__min_row <= self.row_number:
                self._add_to_table_data()

    @property
    def is_str(self) -> bool:
        return self._data_type == XLSTableValueType.STRING

    @abstractmethod
    def iter_rows(self):
        raise NotImplementedError()

    @abstractmethod
    def _set_cell_value(self):
        raise NotImplementedError()

    @abstractmethod
    def _add_to_table_data(self):
        raise NotImplementedError()

    @abstractmethod
    def _set_current_row(self):
        raise NotImplementedError()

    @abstractmethod
    def _set_data_type(self, attrs: AttributesImpl):
        raise NotImplementedError

    def _set_value_from(self):
        if self._data_type:
            self._value_from = self.VALUE_FROM_MAPPING[self._data_type]
