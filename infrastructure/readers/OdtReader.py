from odf import text, teletype
from odf.opendocument import load
from domain.interfaces.FileReader import FileReader

class OdtReader(FileReader):

    def extract(self, path: str) -> str:
        document = load(path)

        paragraphs = document.getElementsByType(
            text.P
        )

        return "\n".join(
            teletype.extractText(paragraph)
            for paragraph in paragraphs
        )