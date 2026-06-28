import re
from core.DocumentPatternsRegex import DOCUMENT_PATTERNS
from domain.models.DocumentType import documentType

class DocumentExtractor:
    @staticmethod
    def extract(
        content: str,
        document_type: documentType
    ) -> dict:

        patterns = DOCUMENT_PATTERNS.get(document_type)
        if patterns is None:
            return {}
        result = {}

        for field, pattern in patterns.items():
            match = re.search(
                pattern,
                content,
                re.DOTALL
            )
            result[field] = (
                match.group(1)
                if match
                else None
            )
        return result