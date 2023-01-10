from lxml_handlers.abstract_lxml_handler import LXMLAbstractHandler
from schemas.table_enums import XLSCellTagNames, XLSTableValueType


class LXMLRawDataHandler(LXMLAbstractHandler):

    def _map_sheet(self, cell):
        self._data_type = cell.get(XLSCellTagNames.DATA_TYPE, XLSTableValueType.UNKNOWN)
        self._set_value_from()
        value = cell.find(self._value_search_pattern)
        return value.text if value is not None else ""

    def _parse_row_child(self, row):
        return list(map(self._map_sheet, row.findall(self._cell_search_pattern)))

    def iter_rows(self):
        for row in self._table_data[0:]:
            yield row

        # self._table_data.append(
        #     list(
        #         map(
        #             self._map_sheet,
        #             row.findall(self._cell_search_pattern),
        #             row.findall(self._value_search_pattern))
        #     )
        # )
