# Sobre o Arquivo

O arquivo `FileReaderFactory` implementa o padrão de projeto **Factory Method**, sendo responsável por centralizar a criação do leitor de arquivos adequado com base na extensão do documento.
# Funcionalidade

Responsabilidade:
- Ela recebe uma [[Document Type e Extension#Document Extension|documentExtension]] e retorna a instância correta do Reader responsável por interpretar aquele tipo de arquivo

## Metódo Get

- O método `get` é estático (`@staticmethod`)
- Recebe como parâmetro a [[Document Type e Extension#Document Extension|documentExtension]]
- Utiliza um Match-Case para decidir qual reader ira instanciar
- Cada `case` registra `logging.debug("Reader escolhido: ...")`; os antigos `print()` foram trocados em 2026-10-18.
- Violação de camadas conhecida: a factory fica em `domain/models`, mas importa os readers de `infrastructure`.

`````python
class FileReaderFactory:

    @staticmethod
    def get(extension: documentExtension):
        match extension:
            case documentExtension.PDF:
                logging.debug("Reader escolhido: pdf")
                return PdfReader()

            case documentExtension.XML:
                logging.debug("Reader escolhido: xml")
                return XmlReader()

            case documentExtension.DOCX:
                logging.debug("Reader escolhido: docx")
                return DocxReader()

            case documentExtension.ODT:
                logging.debug("Reader escolhido: odt")
                return OdtReader()

            case _:
                raise ValueError(f"Nenhum Reader pra extensão: {extension}")
````