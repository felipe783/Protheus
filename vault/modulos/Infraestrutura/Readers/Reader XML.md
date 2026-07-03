O Arquivo `XmlReader` é uma implementação concreta da interface `FileReader`, responsável por extrair texto de arquivos `.xml` 
# Responsabilidade

O objetivo deste arquivo é:
- abrir um arquivo `.xml`
- ler todo o conteúdo textual
# Funcionalidade

- `open(path, "rb")` abre o arquivo `.xml` em modo binário, sem interpretar sua estrutura (tags, encoding declarado etc.)
- `f.read()` lê todo o conteúdo do arquivo como bytes brutos, armazenados em `raw`
- `raw.decode("utf-8")` tenta converter os bytes para texto usando UTF-8, o encoding mais comum
- se a decodificação falhar (`UnicodeDecodeError`), o `except` faz fallback para Latin-1 com `errors="ignore"`, descartando caracteres inválidos em vez de lançar erro


````python
class XmlReader(FileReader):
    def extract(self, path: str) -> str:
        with open(path, "rb") as f:
            raw = f.read()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1", errors="ignore")
````


