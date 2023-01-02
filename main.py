import datetime

from data_extractor import DataExtractor
from schemas import ExtractModes, ExtractEngine

if __name__ == '__main__':
    start = datetime.datetime.now()
    de = DataExtractor('test.xlsx', engine=ExtractEngine.LXML, mode=ExtractModes.GROUP_BY)
    for row in de.iter_rows():
        print(row.dict())
    print((datetime.datetime.now() - start).total_seconds())


# TODO Этапы построения:
# 1. filereader
# 2. convert to yml
# 3. XMLParser
# 4. DataReader
# 5. FilteringData
# 6. Convert to dto
