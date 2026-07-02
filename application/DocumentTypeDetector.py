from core.DocumentKeyWords import KEY_WORDS
from domain.models.DocumentType import documentType
from domain.models.DocumentExtension import documentExtension

class DocumentTypeDetector:

    @staticmethod
    def detect(
        content: str,
        extension: documentExtension
    ) -> documentType:
        content = content.lower()

        if extension == documentExtension.XML:
            if "<nfe" in content:
                return documentType.DANFE_XML

            if "<infnfe" in content:
                return documentType.DANFE_XML

            return documentType.DESCONHECIDO
        scores = {}

        for doc_type, keywords in KEY_WORDS.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in content:
                    score += 1
            scores[doc_type] = score

        best_match = max(scores,key=scores.get)
        if scores[best_match] < 3:
            return documentType.DESCONHECIDO

        return best_match