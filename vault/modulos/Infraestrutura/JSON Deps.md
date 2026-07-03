# Sobre o Arquivo

Este arquivo é responsável por implementar uma camada simples de persistência baseada em arquivo JSON

# Funcionalidade

## Função `get_db`

A função `get_db()` tem como responsabilidade principal garantir o acesso consistente ao banco de dados em formato JSON, primeiramente, ela assegura que o arquivo exista
>caso não exista, ele é criado automaticamente.

Se o arquivo já existir:
- abre o arquivo e realiza o parse do conteúdo em JSON;
- valida se o conteúdo carregado é um `dict`;
- garante que a chave `"documents"` esteja presente na estrutura retornada, assegurando a consistência do formato esperado pela aplicação.

````python
def get_db() -> dict:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        return {"documents": []}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            
        if not isinstance(data, dict):
            return {"documents": []}
            
        data.setdefault("documents", [])
        return data
    except (json.JSONDecodeError, Exception):
        return {"documents": []}
````

## Função `save_db`

A função `save_db(data: dict)` é responsável por persistir os dados no arquivo JSON, ela:
- Garante que o diretório onde o arquivo está localizado existe
>caso não exista, ele é criado automaticamente.
- Em seguida, o arquivo é aberto em modo de escrita, sobrescrevendo completamente o conteúdo anterior, e os dados recebidos são serializados para o formato JSON e gravados no arquivo

````python
def save_db(data: dict) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4, default=str) #Dict -> JSON
````