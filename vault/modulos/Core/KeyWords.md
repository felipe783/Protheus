# Sobre o Arquivo

Esse Módulo cria um **dicionário** chamado `KEY_WORDS` que será usado para identificar automaticamente o tipo de um documento com base nas palavras encontradas em seu conteúdo.
É usando principalmente pelo [[Extrator e Detector#Document Detector detector|DocumentTypeDetector]]
# Funcionalidade:

Cria uma anotação de tipo (_type hint_) para um dicionário em que:
- a **chave** é um valor do enum [[Document Type e Extension#Type type|Document Type]];
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