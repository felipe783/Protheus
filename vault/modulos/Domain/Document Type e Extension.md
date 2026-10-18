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

É um enum `documentExtension` que representa as **extensões de arquivo suportadas**. O valor de cada membro já inclui o ponto (`".pdf"`), porque é comparado diretamente com `Path(filename).suffix` no `DocumentExtensionDetector`.

````python
class documentExtension(str, Enum):
    PDF = ".pdf"
    XML = ".xml"
    DOCX = ".docx"
    ODT = ".odt"
    DESCONHECIDO = ""
````

> [!note] Efeito colateral do ponto no valor
> O [[Controller (Protheus)|Controller]] cria o temporário com `suffix=f".{extension.value}"`, o que gera `arquivo..pdf` (dois pontos). Funciona porque os readers não dependem do nome do arquivo, mas o ponto extra é redundante.
