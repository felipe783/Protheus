# Sobre o Arquivo

O arquivo "Patterns" tem como responsabilidade centralizar todos os padrões de extração de dados dos documentos suportados pelo sistema.
- Cada tipo de [Regex](https://regexr.com/) é separado por cada documento(crlv,nfe,cartão cnpj)
- E centraliza tudo em uma ``única Dict`` chamada de ``DOCUMENT_PATTERNS`` ,funcionando como um catalogo onde a chave é o [[Document Type e Extension#Document Type|DocumentType]]

````python
NFE_PATTERNS = {
    "chave_acesso": r"<chNFe>(\d{44})</chNFe>",
    "numero_nota": r"<nNF>(\d+)</nNF>",
	...
}
CNPJ_PATTERNS = {
    "cnpj": r"NÚMERO\s*DE\s*INSCRIÇÃO\s*([\d./-]+)",
    "nome_fantasia": r"TÍTULO\s*DO\s*ESTABELECIMENTO.*?\n([\s\S]*?)\s*PORTE",
    ...
}
CRLV_PATTERNS = {
    "placa": r"PLACA\s*:?\s*([A-Z]{3}\d[A-Z0-9]\d{2})",
    "renavam": r"RENAVAM\s*:?\s*(\d{11})",
    ...
}
DOCUMENT_PATTERNS = {
    documentType.DANFE_XML: NFE_PATTERNS,
    documentType.CARTAO_CNPJ: CNPJ_PATTERNS,
    documentType.CRLV_E: CRLV_PATTERNS,

}
````

> [!warning] Tipos sem padrões
> `LAUDO` e `CONTRATO` não estão em `DOCUMENT_PATTERNS`. Eles podem ser classificados (têm [[KeyWords (Protheus)|KeyWords]]), mas o `DocumentExtractor` retorna `{}` para eles.
