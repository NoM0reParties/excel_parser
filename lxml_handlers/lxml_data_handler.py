from typing import Optional, List

from lxml_handlers.abstract_lxml_handler import LXMLAbstractHandler
from schemas import XMLTableDataCell, XMLTableDataRow
from schemas.table_enums import XLSCellTagNames, XLSTableValueType, XLSRowTagNames


class LXMLDataHandler(LXMLAbstractHandler):

    @property
    def headers(self) -> Optional[List[Optional[str]]]:
        if self._table_data:
            return [h.value for h in self._table_data[0]]

    def _map_sheet(self, cell):
        self._data_type = cell.get(XLSCellTagNames.DATA_TYPE, XLSTableValueType.UNKNOWN)
        self._set_value_from()
        value = cell.find(self._value_search_pattern)
        return XMLTableDataCell(
            cell_coords=cell.get(XLSCellTagNames.COORDS),
            value=value.text if value is not None else None
        )

    def _parse_row_child(self, row):
        data_row = XMLTableDataRow(
            row_number=int(row.attrib.get(XLSRowTagNames.ROW_NUMBER)),
            columns=self.headers
        )
        data_row.set_cells(list(map(self._map_sheet, row.findall(self._cell_search_pattern))))
        return data_row

    def iter_rows(self):
        for row in self._table_data[1:]:
            yield row
