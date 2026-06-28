NFE_PATTERNS = {
    "chave_acesso": r"<chNFe>(\d{44})</chNFe>",
    "numero_nota": r"<nNF>(\d+)</nNF>",
    "serie": r"<serie>(\d+)</serie>",
    "cnpj_emitente": r"<emit>.*?<CNPJ>(\d+)</CNPJ>",
    "valor_total": r"<vNF>([\d.]+)</vNF>",
}

CNPJ_PATTERNS = {
    "cnpj": r"<cnpj>(\d+)</cnpj>",
    "razao_social": r"<razaoSocial>(.*?)</razaoSocial>",
    "nome_fantasia": r"<nomeFantasia>(.*?)</nomeFantasia>",
    "situacao": r"<situacaoCadastral>(.*?)</situacaoCadastral>",
}

CRLV_PATTERNS = {
    "placa": r"<placa>(.*?)</placa>",
    "renavam": r"<renavam>(\d+)</renavam>",
    "ano_exercicio": r"<exercicio>(\d+)</exercicio>",
    "chassi": r"<chassi>(.*?)</chassi>",
}