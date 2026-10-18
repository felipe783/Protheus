# Sobre o Arquivo

Esse Módulo cria um **dicionário** chamado `KEY_WORDS` que será usado para identificar automaticamente o tipo de um documento com base nas palavras encontradas em seu conteúdo.
É usando principalmente pelo [[Extrator e Detector#Document Detector|DocumentTypeDetector]]
# Funcionalidade:

Cria uma anotação de tipo (_type hint_) para um dicionário em que:
- a **chave** é um valor do enum [[Document Type e Extension#Document Type|Document Type]];
- o **valor** é uma lista de strings (`list[str]`).

````python
KEY_WORDS: dict[documentType, list[str]] = {
    documentType.CRLV_E: [
        "CRLV-e",
        "CERTIFICADO DE REGISTRO E LICENCIAMENTO DE VEÍCULO",
        "PLACA",
        "RENAVAM",
		...
    ],
    documentType.CARTAO_CNPJ: [
        "NÚMERO DE INSCRIÇÃO",
        "DATA DE ABERTURA",
        "NOME EMPRESARIAL",
		...
    ]
````

- O código também tem listas para `DANFE_XML`, `LAUDO` e `CONTRATO` (omitidas acima).
- O detector exige **pelo menos 3 palavras-chave** encontradas; abaixo disso o tipo é `DESCONHECIDO`.
- `LAUDO` e `CONTRATO` têm palavras-chave mas não têm [[Patterns (Protheus)|Patterns]], então são classificados sem extração de campos.
