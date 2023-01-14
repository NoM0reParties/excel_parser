import datetime

from data_extractor import DataExtractor
from schemas import ExtractModes, ExtractEngine

if __name__ == '__main__':
    start = datetime.datetime.now()
    de = DataExtractor(
        'test_big.xlsx',
        engine=ExtractEngine.SAX,
        mode=ExtractModes.GROUP_BY,
        min_row=1,
        sheet_name="svod_SKU"
    )
    for row in de.iter_rows():
        for cell in row:
            print(cell)
    print((datetime.datetime.now() - start).total_seconds())


# TODO Этапы построения:
# 1. filereader
# 2. convert to yml
# 3. XMLParser
# 4. DataReader
# 5. FilteringData
# 6. Convert to dto
