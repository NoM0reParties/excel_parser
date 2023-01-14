from typing import Dict
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl


class WorkbookHandler(ContentHandler):

    def __init__(self):
        super().__init__()
        self.file_name_to_id_mapping: Dict[str, str] = {}

    def startElement(self, name: str, attrs: AttributesImpl):
        if name == "sheet":
            self.file_name_to_id_mapping.setdefault(attrs.get("name"), attrs.get("sheetId"))
