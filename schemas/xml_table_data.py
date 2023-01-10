import re
from typing import Optional, List, Any


class XMLTableDataCell:

    def __init__(self, cell_coords: str, value: str):
        self.cell_coords = cell_coords
        self.value = value

    @property
    def col(self) -> str:
        raw_result = re.search(r'^[a-zA-Z]{1,3}', self.cell_coords)
        return raw_result.group()

    @property
    def row(self) -> int:
        raw_result = re.search(r'\d{1,3}', self.cell_coords)
        return int(raw_result.group())

    def set_value(self, value: str):
        self.value = value

    def __str__(self):
        return f'XMLTableDataCell\ncoords: {self.cell_coords}\nvalue: {self.value}\n'

    @property
    def typed_value(self) -> Any:
        if self.value is None:
            return
        raw_symbols = self.value.replace(',', '').replace('.', '')
        if not raw_symbols.isdigit():
            return self.value
        decimal_part = self.value.split('.')
        if len(decimal_part) == 1:
            return int(self.value)
        if re.search(r'^0{1,100}$', decimal_part[1]):
            return int(decimal_part[0])
        return float(self.value)


class XMLTableDataRow:

    def __init__(self, row_number: int, columns: List[str]):
        self.row_number = row_number
        self.cells: List[XMLTableDataCell] = []
        self.columns: List[str] = columns

    def __add__(self, cell: XMLTableDataCell):
        self.cells.append(cell)

    def __repr__(self) -> str:
        return f"XMLTableDataRow(row_number: {self.row_number} cells_count: {len(self.cells)})"

    def __iter__(self):
        self._iter_count = 0
        return self

    def __next__(self) -> XMLTableDataCell:
        if self._iter_count < len(self.cells):
            cell = self.cells[self._iter_count]
            self._iter_count += 1
            return cell
        else:
            raise StopIteration

    def __column_index_by_name(self, key: Optional[str] = None):
        if key is not None:
            try:
                return self.columns.index(key)
            except IndexError:
                raise ValueError("No such header find. Check if there are any mistakes in `key` string")
        return 0

    def dict_by_key(self, key: Optional[str] = None) -> dict:
        row_key = None
        values = {}
        main_column = self.__column_index_by_name(key=key)
        for i, c in enumerate(self.cells):
            if i == main_column:
                row_key = c.value
                continue
            values.setdefault(self.columns[i], c.value)
        return {row_key: values}

    def dict(self):
        return {self.columns[i]: c.typed_value for i, c in enumerate(self.cells)}

    def dict_by_col(self):
        return {c.col: c.typed_value for c in self.cells}

    def set_cells(self, cells):
        self.cells = cells
