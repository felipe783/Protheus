O Arquivo `DocxReader` é uma implementação concreta da interface `FileReader`, responsável por extrair texto de arquivos `.docx` (Microsoft Word).
##  Responsabilidade

O objetivo deste arquivo é:
- abrir um arquivo `.docx`
- ler todo o conteúdo textual
# Funcionalidade

- `DocxDocument(path)` abre o arquivo `.docx` e retorna um objeto `Document`
- `doc.paragraphs` retorna a lista de parágrafos do corpo do documento, na ordem original
- `paragraph.text` extrai o texto puro de cada parágrafo, sem formatação
- `"\n".join(...)` junta tudo em uma única string, separando os parágrafos por quebra de linha


````python
class DocxReader(FileReader):
    def extract(self, path: str) -> str:
        doc = DocxDocument(path)
        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )
````
