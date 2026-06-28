import re
from pathlib import Path
from domain.models.DocumentType import documentType
from core.DocumentKeyWords import KEY_WORDS
import xml.etree.ElementTree as ET

def readXml(file_path: str):
    tree = ET.parse(file_path)
    return tree.getroot()

def getDocumentType(content: str) -> documentType:
    content = content.lower()

    scores = {}

    for doc_type, keywords in KEY_WORDS.items():
        scores[doc_type] = sum(
            1 for keyword in keywords
            if keyword.lower() in content
        )

    best_match = max(scores, key=scores.get)

    if scores[best_match] == 0:
        return documentType.DESCONHECIDO

    return best_match

def extractPdfText(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


