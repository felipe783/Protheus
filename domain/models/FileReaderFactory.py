from domain.models.DocumentExtension import documentExtension
from infrastructure.readers.PdfReader import PdfReader
from infrastructure.readers.XmlReader import XmlReader
from infrastructure.readers.DocxReader import DocxReader
from infrastructure.readers.OdtReader import OdtReader

class FileReaderFactory:
    @staticmethod
    def get(extension: documentExtension):
        match extension:
            
            case documentExtension.PDF:
                print("pdf")
                return PdfReader()
            
            case documentExtension.XML:
                print("xml")
                return XmlReader()

            case documentExtension.DOCX:
                print("docx")
                return DocxReader()

            case documentExtension.ODT:
                print("odt")
                return OdtReader()

            case _:
                raise ValueError(
                    f"Nenhum Reader pra extensão: {extension}"
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