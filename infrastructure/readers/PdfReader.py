from pypdf import PdfReader as PyPdfReader
from domain.interfaces.FileReader import FileReader

class PdfReader(FileReader):

    def extract(self, path: str) -> str:
        reader = PyPdfReader(path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)