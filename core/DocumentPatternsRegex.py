from domain.models.DocumentType import documentType

NFE_PATTERNS = {
    "chave_acesso": r"<chNFe>(\d{44})</chNFe>",
    "numero_nota": r"<nNF>(\d+)</nNF>",
    "serie": r"<serie>(\d+)</serie>",
    "cnpj_emitente": r"<emit>.*?<CNPJ>(\d+)</CNPJ>",
    "valor_total": r"<vNF>([\d.]+)</vNF>",
}

CNPJ_PATTERNS = {
    "cnpj": r"NÚMERO\s*DE\s*INSCRIÇÃO\s*([\d./-]+)",
    "razao_social": r"NOME\s*EMPRESARIAL\s*([\s\S]*?)\s*TÍTULO\s*DO\s*ESTABELECIMENTO",
    "nome_fantasia": r"TÍTULO\s*DO\s*ESTABELECIMENTO.*?\n([\s\S]*?)\s*PORTE", 
    "data_criacao": r"DATA\s*DE\s*ABERTURA\s*([\d]{2}/[\d]{2}/[\d]{4})", 
    "situacao": r"SITUAÇÃO\s*CADASTRAL\s*(ATIVA|BAIXADA|SUSPENSA|INAPTA|NULA)", 
    "nome_socio": r"([^\n\r]+)\s+SÓCIO-ADMINISTRADOR",
}

CRLV_PATTERNS = {
    "placa": r"PLACA\s*:?\s*([A-Z]{3}\d[A-Z0-9]\d{2})",
    "renavam": r"RENAVAM\s*:?\s*(\d{11})",
    "chassi": r"CHASSI\s*:?\s*([A-HJ-NPR-Z0-9]{17})",
    "marca_modelo": r"MARCA/?MODELO\s*:?\s*([\s\S]*?)\s*ANO",
    "ano_fabricacao": r"ANO\s*FABRICAÇÃO/?MODELO\s*:?\s*(\d{4})/\d{4}",
    "ano_modelo": r"ANO\s*FABRICAÇÃO/?MODELO\s*:?\s*\d{4}/(\d{4})",
    "combustivel": r"COMBUSTÍVEL\s*:?\s*([^\n\r]+)",
    "cor": r"COR\s*:?\s*([^\n\r]+)",
    "categoria": r"CATEGORIA\s*:?\s*([^\n\r]+)",
    "proprietario": r"PROPRIETÁRIO\s*:?\s*([^\n\r]+)",
    "cpf": r"CPF\s*:?\s*([\d.-]{11,14})",
    "municipio": r"MUNICÍPIO\s*:?\s*([^\n\r]+)",
    "licenciamento": r"(?:EXERCÍCIO\s*DO\s*)?LICENCIAMENTO\s*:?\s*(\d{4})",
}

DOCUMENT_PATTERNS = {
    documentType.DANFE_XML: NFE_PATTERNS,
    documentType.CARTAO_CNPJ: CNPJ_PATTERNS,
    documentType.CRLV_E: CRLV_PATTERNS,
}