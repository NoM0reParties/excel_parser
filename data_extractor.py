from data_extractor_factory import DataExtractorFactory
from schemas import ExtractModes, ExtractEngine


class DataExtractor:

    def __init__(
            self,
            file_name: str,
            mode: ExtractModes = ExtractModes.SIMPLE,
            min_row: int = 1,
            engine: ExtractEngine = ExtractEngine.LXML
    ):
        self.__factory = DataExtractorFactory
        reader, data_handler = self.__factory.get_reader_and_handler(
            mode=mode,
            engine=engine
        )
        self.__file_reader = reader(
            file_name=file_name,
            data_handler=data_handler,
            min_row=min_row,
        )
        self.__data_read = False

    def read_data(self):
        if not self.__data_read:
            self.__file_reader.read()
        self.__data_read = True

    def iter_rows(self):
        self.read_data()
        return self.__file_reader.iter_rows()

