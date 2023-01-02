from typing import List, Optional

from schemas import XLSCellTagNames
from sax_handlers.asbtract_xml_handler import AbstractXmlHandler


class RawTableDataHandler(AbstractXmlHandler):

    def __init__(self, min_row: int = 1):
        super().__init__(min_row=min_row)
        self._current_row: Optional[List[str]] = []
        self._table_data: List[List[str]] = []
        self._current_cell: str = ""

    def _set_current_row(self):
        self._current_row = []

    def _set_cell_value(self):
        value = self.strings_mapping[int(self._tag_content)] if self.is_str else self._tag_content
        self._current_cell = value
        self._current_row.append(self._current_cell)

    def _add_to_table_data(self):
        self._table_data.append(self._current_row)

    def _set_data_type(self, attrs):
        self._data_type = attrs.get(XLSCellTagNames.DATA_TYPE)

    def iter_rows(self):
        for row in self._table_data[1:]:
            yield row
