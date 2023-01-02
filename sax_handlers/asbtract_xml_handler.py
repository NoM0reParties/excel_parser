from abc import abstractmethod
from typing import Optional, List
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl

from schemas import XLSTableValueType, XLSTagTypes, XLSRowTagNames


class AbstractXmlHandler(ContentHandler):

    def __init__(self, min_row: int = str):
        super().__init__()
        self.row_number = 0
        self._current_el: Optional[str] = None
        self.strings_mapping: List[str] = []
        self._tag_content: str = ""
        self._data_type: str = ""
        self._iter_count: int = 0
        self.__min_row = min_row

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
        if name == XLSTagTypes.VALUE:
            self._set_cell_value()
        if name == XLSTagTypes.ROW:
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
