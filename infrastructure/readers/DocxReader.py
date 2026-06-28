from docx import Document as DocxDocument
from domain.interfaces.FileReader import FileReader

class DocxReader(FileReader):

    def extract(self, path: str) -> str:
        doc = DocxDocument(path)

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )