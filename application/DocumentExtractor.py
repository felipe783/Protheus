import re
from core.DocumentPatternsRegex import DOCUMENT_PATTERNS
from domain.models.DocumentType import documentType

class DocumentExtractor:

    @staticmethod
    def extract(content: str, document_type: documentType) -> dict:
        patterns = DOCUMENT_PATTERNS.get(document_type)
        if not patterns:
            return {}
        result = {}
        flags = re.DOTALL | re.MULTILINE
        for field, pattern in patterns.items():
            match = re.search(pattern, content, flags)
            if match:
                value = re.sub(r"\s+", " ", match.group(1)).strip()
            else:
                value = None
            result[field] = value

        return result