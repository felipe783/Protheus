from enum import Enum


class TypeExtension(str, Enum):
    PDF = ".pdf"
    XML = ".xml"
    DOCX = ".docx"
    ODT = ".odt"