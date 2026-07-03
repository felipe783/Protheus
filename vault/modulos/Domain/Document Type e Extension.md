# Sobre os Arquivos

As classes `documentType` e `documentExtension` são **enums tipados como `str`**, o que significa que cada valor do enum também se comporta como uma string. 
# Document Type^type

É um enum `documentType` representa a **classificação lógica do documento**, independentemente do formato do arquivo. Ela define os possíveis tipos reconhecidos

````python
class documentType(str, Enum):
    CRLV_E = "crlv_e"
    CARTAO_CNPJ = "cartao_cnpj"
    DANFE_XML = "danfe_xml"
    LAUDO = "laudo"
    CONTRATO = "contrato"
    DESCONHECIDO = "desconhecido"
````

# Document Extension ^extension

É um enum `documentExtension` representa a **classificação lógica da extensão documento**, independentemente do formato do arquivo.

````python
class documentType(str, Enum):
    CRLV_E = "crlv_e"
    CARTAO_CNPJ = "cartao_cnpj"
    DANFE_XML = "danfe_xml"
    LAUDO = "laudo"
    CONTRATO = "contrato"
    DESCONHECIDO = "desconhecido"
````