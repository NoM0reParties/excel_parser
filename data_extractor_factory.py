from file_readers import *
from lxml_handlers import LXMLRawDataHandler, LXMLDataHandler
from sax_handlers.data_handlers.raw_table_data_handler import RawTableDataHandler
from sax_handlers.data_handlers.table_data_handler import TableDataHandler
from schemas import ExtractEngine, ExtractModes


class DataExtractorFactory:

    @staticmethod
    def get_reader_and_handler(mode: ExtractModes, engine: ExtractEngine):
        reader = LXMLFileReader if engine == ExtractEngine.LXML else SaxFileReader
        data_handler = None
        if engine == ExtractEngine.SAX:
            if mode == ExtractModes.SIMPLE:
                data_handler = RawTableDataHandler
            elif mode == ExtractModes.GROUP_BY:
                data_handler = TableDataHandler
        elif engine == ExtractEngine.LXML:
            if mode == ExtractModes.SIMPLE:
                data_handler = LXMLRawDataHandler
            elif mode == ExtractModes.GROUP_BY:
                data_handler = LXMLDataHandler
        return reader, data_handler
