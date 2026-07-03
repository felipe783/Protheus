O Arquivo `PdfReader` é uma implementação concreta da interface `FileReader`, responsável por extrair texto de arquivos `.pdf` 
# Responsabilidade

O objetivo deste arquivo é:
- abrir um arquivo `.pdf`
- ler todo o conteúdo textual
# Funcionalidade

- `PyPdfReader(path)` abre o arquivo `.pdf` e retorna um objeto `reader`, dando acesso às páginas do documento
- `reader.pages` retorna a lista de páginas do PDF, na ordem original
- `page.extract_text()` extrai o texto puro de cada página; pode retornar `None` ou string vazia quando a página não tem texto extraível (ex.: página escaneada como imagem)
- o `if page_text` filtra páginas sem texto, evitando entradas vazias/`None` na lista
- `"\n".join(text)` junta o texto das páginas válidas em uma única string, separando por quebra de linha

````python
class PdfReader(FileReader):
    def extract(self, path: str) -> str:
        reader = PyPdfReader(path)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return "\n".join(text)
````

