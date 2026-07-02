import re
from core.DocumentPatternsRegex import DOCUMENT_PATTERNS
from domain.models.DocumentType import documentType

class DocumentExtractor:

    @staticmethod
    def extract(content: str, document_type: documentType) -> dict:
        patterns = DOCUMENT_PATTERNS.get(document_type)
        if not patterns:
            return {}
        if document_type != documentType.DANFE_XML: #NFE Pq ela é especial(.xml)
            content = content.upper()

        result = {}
        flags = re.DOTALL | re.MULTILINE
        for field, pattern in patterns.items():
            match = re.search(pattern, content, flags)
            value = re.sub(r"\s+", " ", match.group(1)).strip() if match else None
            result[field] = value

        return result