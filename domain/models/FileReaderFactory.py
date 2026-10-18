import logging
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
                logging.debug("Reader escolhido: pdf")
                return PdfReader()
            
            case documentExtension.XML:
                logging.debug("Reader escolhido: xml")
                return XmlReader()

            case documentExtension.DOCX:
                logging.debug("Reader escolhido: docx")
                return DocxReader()

            case documentExtension.ODT:
                logging.debug("Reader escolhido: odt")
                return OdtReader()

            case _:
                raise ValueError(f"Nenhum Reader pra extensão: {extension}")