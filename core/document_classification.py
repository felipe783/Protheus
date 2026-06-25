from Protheus.domain.models.document_type import documentType

KEY_WORDS: dict[documentType, list[str]] = {
    documentType.CRLV_E: [
        "crlv", "certificado de registro e licenciamento", "renavam",
        "licenciamento de veiculo", "exercicio",
    ],
    documentType.CARTAO_CNPJ: [
        "cartao cnpj", "comprovante de inscricao", "cadastro nacional da pessoa juridica",
        "situacao cadastral", "receita federal",
    ],
    documentType.DANFE_XML: [
        "danfe", "nota fiscal eletronica", "nfe", "chave de acesso",
        "protocolo de autorizacao", "documento auxiliar da nota fiscal",
    ],
    documentType.LAUDO: [
        "laudo", "laboratorio", "analise laboratorial", "resultado de exame", "amostra",
    ],
    documentType.CONTRATO: [
        "contrato", "contratante", "contratada", "clausula", "rescisao", "multa",
        "partes contratantes",
    ],
}
