from domain.models.DocumentExtension import documentExtension
from infrastructure.readers.PdfReader import PdfReader
from infrastructure.readers.XmlReader import XmlReader
from infrastructure.readers.DocxReader import DocxReader
from infrastructure.readers.OdtReader import OdtReader

class FileReaderFactory:
    @staticmethod
    def create(extension: documentExtension):
        match extension:
            
            case documentExtension.PDF:
                return PdfReader()
            
            case documentExtension.XML:
                return XmlReader()

            case documentExtension.DOCX:
                return DocxReader()

            case documentExtension.ODT:
                return OdtReader()

            case _:
                raise ValueError(
                    f"Extensão não suportada: {extension}"
                )
            

"""
Arquivo
 ↓
FileReaderFactory
 ↓
Conteúdo
 ↓
DocumentDetector
 ↓
DocumentType
 ↓
DocumentExtractorFactory
 ↓
Dados extraídos
"""