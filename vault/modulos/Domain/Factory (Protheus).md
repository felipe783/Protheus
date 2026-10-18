# Sobre o Arquivo

O arquivo `FileReaderFactory` implementa o padrão de projeto **Factory Method**, sendo responsável por centralizar a criação do leitor de arquivos adequado com base na extensão do documento.
# Funcionalidade

Responsabilidade:
- Ela recebe uma [[Document Type e Extension#Document Extension extension|documentExtension]] e retorna a instância correta do Reader responsável por interpretar aquele tipo de arquivo

## Metódo Get

- O método `get` é estático (`@staticmethod`)
- Recebe como parâmetro a [[Document Type e Extension#Document Extension extension|documentExtension]]
- Utiliza um Match-Case para decidir qual reader ira instanciar
- No código atual os `print("pdf")`, `print("xml")` etc. estão **ativos** (o trecho abaixo os mostra comentados); o ideal seria trocá-los por `logging.debug`.

`````python
class FileReaderFactory:

    @staticmethod
    def get(extension: documentExtension):
        match extension:
            case documentExtension.PDF:
                #print("pdf")
                return PdfReader()

            case documentExtension.XML:
                #print("xml")
                return XmlReader()

            case documentExtension.DOCX:
                #print("docx")
                return DocxReader()

            case documentExtension.ODT:
                #print("odt")
                return OdtReader()

            case _:
                raise ValueError(f"Nenhum Reader pra extensão: {extension}")
````