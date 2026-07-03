O Arquivo `OdtReader` é uma implementação concreta da interface `FileReader`, responsável por extrair texto de arquivos `.odt` (LibreOffice Writer/ Apache OpenOffice Writer).
# Responsabilidade

O objetivo deste arquivo é:
- abrir um arquivo `.odt`
- ler todo o conteúdo textual
# Funcionalidade

- `load(path)` abre o arquivo `.odt` e retorna um objeto `document`, no formato manipulável da biblioteca `odfpy`
- `document.getElementsByType(text.P)` retorna a lista de elementos do tipo parágrafo (`<text:p>`) presentes no documento
- `teletype.extractText(paragraph)` extrai o texto puro de cada parágrafo, sem marcações do XML interno do ODT
- `"\n".join(...)` junta tudo em uma única string, separando os parágrafos por quebra de linha


````python
class OdtReader(FileReader):
    def extract(self, path: str) -> str:
        document = load(path)
        paragraphs = document.getElementsByType(text.P)
        return "\n".join(
            teletype.extractText(paragraph)
            for paragraph in paragraphs
        )
````

