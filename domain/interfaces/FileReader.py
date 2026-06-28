from abc import ABC, abstractmethod

class FileReader(ABC):

    @abstractmethod
    def extract(self, path: str) -> str:
        pass

class PdfReader(FileReader):
    ...

class XmlReader(FileReader):
    ...

class DocxReader(FileReader):
    ...