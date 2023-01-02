from lxml_handlers.abstract_lxml_handler import LXMLAbstractHandler
from schemas.table_enums import XLSCellTagNames, XLSTableValueType


class LXMLRawDataHandler(LXMLAbstractHandler):

    def _map_sheet(self, cell, value):
        d_type = cell.get(XLSCellTagNames.DATA_TYPE)
        return value.text if d_type == XLSTableValueType.NUMBER else self._shared_strings[int(value.text)]

    def _parse_row_child(self, row, number):
        self._table_data.append(
            list(
                map(
                    self._map_sheet,
                    row.findall(self._cell_search_pattern),
                    row.findall(self._value_search_pattern))
            )
        )
