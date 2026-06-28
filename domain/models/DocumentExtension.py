from enum import Enum

class documentExtension(str, Enum):
    PDF = ".pdf"
    XML = ".xml"
    DOCX = ".docx"
    ODT = ".odt"
    DESCONHECIDO = ""