# Sobre o Arquivo

Esse Arquivo define uma **classe abstrata**,o objetivo é garantir que qualquer classe responsável por ler um arquivo implemente o método `extract`.

# Funcionalidade

Primeiramente é criada a classe `FileReader`, que herda de `ABC` (_Abstract Base Class_), tornando-a uma classe abstrata. 
- Nela é declarado o método abstrato `extract`, que recebe o caminho do arquivo (`path: str`) e deve retornar uma `string` contendo o conteúdo extraído
- A partir dessa classe são criadas as classes concretas, como `PdfReader`, `XmlReader` e `DocxReader`, que herdam de `FileReader` e implementam o método `extract` de acordo com as particularidades de cada formato de arquivo.
- Caso alguma classe herde de `FileReader` e não implemente o método `extract`, o Python impedirá sua instanciação

````python
class FileReader(ABC):
    @abstractmethod
    def extract(self, path: str) -> str:
        pass

class PdfReader(FileReader):
    ...

class XmlReader(FileReader):
    ...

class DocxReader(FileReader):
    ...
````