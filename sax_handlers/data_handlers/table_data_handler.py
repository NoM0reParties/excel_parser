from typing import List, Optional

from schemas import XMLTableDataCell, XMLTableDataRow, XLSCellTagNames, XLSTableValueType
from sax_handlers.asbtract_xml_handler import AbstractXmlHandler


class TableDataHandler(AbstractXmlHandler):

    def __init__(self, min_row: int = 1):
        super().__init__(min_row=min_row)
        self._current_row: Optional[XMLTableDataRow] = None
        self._table_data: List[XMLTableDataRow] = []
        self._current_cell: Optional[XMLTableDataCell] = None

    def _set_data_type(self, attrs):
        cell_coords = attrs.get(XLSCellTagNames.COORDS)
        self._data_type = attrs.get(XLSCellTagNames.DATA_TYPE, XLSTableValueType.UNKNOWN)
        self._set_value_from()
        self._current_cell = XMLTableDataCell(
            cell_coords=cell_coords,
            value=''
        )

    def _set_current_row(self):
        self._current_row = XMLTableDataRow(
            row_number=self.row_number,
            columns=self.headers
        )

    @property
    def headers(self) -> Optional[List[Optional[str]]]:
        if self._table_data:
            return [h.value for h in self._table_data[0]]

    def find_header_index(self, header: str) -> int:
        return self.headers.index(header)

    def iter_rows(self):
        for row in self._table_data[1:]:
            yield row

    def _set_cell_value(self):
        value = self.strings_mapping[int(self._tag_content)] if self.is_str else self._tag_content
        self._current_cell.set_value(value)
        self._current_row + self._current_cell

    def _add_to_table_data(self):
        self._table_data.append(self._current_row)
