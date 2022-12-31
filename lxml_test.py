import datetime
from zipfile import ZipFile

from lxml import etree as ET





start = datetime.datetime.now()

print("running with lxml.etree")

zf = ZipFile('test.xlsx')

tree = ET.parse(zf.open('xl/sharedStrings.xml'))
root = tree.getroot()
result1 = list(map(lambda x: x.text, root.findall('.//{*}t')))

def mao_sheet(a, b):
    dtype = a.get('t')
    return b.text if dtype == 'n' else result1[int(b.text)]

tree = ET.parse(zf.open('xl/worksheets/sheet1.xml'))
root = tree.getroot()
result2 = list(map(mao_sheet, root.findall('.//{*}c'), root.findall('.//{*}v')))
print(result2)

print((datetime.datetime.now() - start).total_seconds())