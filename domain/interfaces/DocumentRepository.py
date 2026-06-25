from abc import ABC, abstractmethod

class DocumentRepository(ABC):
    
    @abstractmethod
    def save(self, document):
        pass