from typing import Optional, List
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl


class SharedStringHandler(ContentHandler):

    def __init__(self):
        super().__init__()
        self._current_el: Optional[str] = None
        self.strings_mapping: List[str] = []
        self._tag_content: str = ""

    def startElement(self, name: str, attrs: AttributesImpl):
        self._tag_content = ""
        self._current_el = name

    def characters(self, content):
        self._tag_content += content

    def endElement(self, name: str):
        if name == 't':
            self.strings_mapping.append(self._tag_content)
