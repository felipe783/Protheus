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
    "nome_socio": r"([^\n\r]+)\s+Sócio-Administrador"
}

CRLV_PATTERNS = {
    "placa": r"<placa>(.*?)</placa>",
    "renavam": r"<renavam>(\d+)</renavam>",
    "ano_exercicio": r"<exercicio>(\d+)</exercicio>",
    "chassi": r"<chassi>(.*?)</chassi>",
}

DOCUMENT_PATTERNS = {
    documentType.DANFE_XML: NFE_PATTERNS,
    documentType.CARTAO_CNPJ: CNPJ_PATTERNS,
    documentType.CRLV_E: CRLV_PATTERNS,
}