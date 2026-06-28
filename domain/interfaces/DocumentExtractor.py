from abc import ABC, abstractmethod

class DocumentExtractor(ABC):
    
    @abstractmethod
    def extract(self, content: str) -> dict:
        pass