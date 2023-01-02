from typing import Optional, List

from lxml_handlers.abstract_lxml_handler import LXMLAbstractHandler
from schemas import XMLTableDataCell, XMLTableDataRow
from schemas.table_enums import XLSCellTagNames, XLSTableValueType


class LXMLDataHandler(LXMLAbstractHandler):

    @property
    def headers(self) -> Optional[List[Optional[str]]]:
        if self._table_data:
            return [h.value for h in self._table_data[0]]

    def _map_sheet(self, cell, value):
        d_type = cell.get(XLSCellTagNames.DATA_TYPE)
        return XMLTableDataCell(
            cell_coords=cell.get(XLSCellTagNames.COORDS),
            value=value.text if d_type == XLSTableValueType.NUMBER else self._shared_strings[int(value.text)]
        )

    def _parse_row_child(self, row, number):
        data_row = XMLTableDataRow(
            row_number=number,
            columns=self.headers
        )
        data_row.set_cells(
            list(
                map(
                    self._map_sheet,
                    row.findall(self._cell_search_pattern),
                    row.findall(self._value_search_pattern),
                )
            )
        )
        self._table_data.append(data_row)
