from enum import Enum


class TypeDocument(str, Enum):
    CRLV_E = "crlv_e"
    CARTAO_CNPJ = "cartao_cnpj"
    DANFE_XML = "danfe_xml"
    LAUDO = "laudo"
    CONTRATO = "contrato"
    DESCONHECIDO = "desconhecido"