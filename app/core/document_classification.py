from domain.models.type_document import TypeDocument

KEY_WORDS: dict[TypeDocument, list[str]] = {
    TypeDocument.CRLV_E: [
        "crlv", "certificado de registro e licenciamento", "renavam",
        "licenciamento de veiculo", "exercicio",
    ],
    TypeDocument.CARTAO_CNPJ: [
        "cartao cnpj", "comprovante de inscricao", "cadastro nacional da pessoa juridica",
        "situacao cadastral", "receita federal",
    ],
    TypeDocument.DANFE_XML: [
        "danfe", "nota fiscal eletronica", "nfe", "chave de acesso",
        "protocolo de autorizacao", "documento auxiliar da nota fiscal",
    ],
    TypeDocument.LAUDO: [
        "laudo", "laboratorio", "analise laboratorial", "resultado de exame", "amostra",
    ],
    TypeDocument.CONTRATO: [
        "contrato", "contratante", "contratada", "clausula", "rescisao", "multa",
        "partes contratantes",
    ],
}
