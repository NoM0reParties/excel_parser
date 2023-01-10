from enum import Enum


class ExtractModes(str, Enum):
    SIMPLE = 'SIMPLE'
    GROUP_BY = 'GROUP_BY'


class ExtractEngine(str, Enum):
    SAX = 'SAX'
    LXML = 'LXML'


class XLSTagTypes(str, Enum):
    CELL = 'c'
    VALUE = 'v'
    FORMULA = 'f'
    ROW = 'row'
    INLINE_STRING = 't'
    UNKNOWN = 'UNKNOWN'


class XLSTableValueType(str, Enum):
    STRING = 's'
    NUMBER = 'n'
    INLINE_STRING = 'inlineStr'
    UNKNOWN = 'UNKNOWN'


class XLSCellTagNames(str, Enum):
    COORDS = 'r'
    DATA_TYPE = 't'
    STYLE = 's'


class XLSRowTagNames(str, Enum):
    ROW_NUMBER = 'r'
