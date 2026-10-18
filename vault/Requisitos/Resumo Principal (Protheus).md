### Linguagem Principal

``Python``
### Upload de Documentos

O usuário deve poder fazer upload dos seguintes tipos de arquivo:
- CRLV-e
- Cartão CNPJ
- DANFEs/XMLs
- Laudos laboratoriais
**Extensões aceitas:**
- PDF
- XML
- DOCX
- ODT
### Extração dos Dados

A extração varia conforme o tipo e a extensão do arquivo:

- **PDF** — leitura e extração de texto feitas com a biblioteca `pypdf`. 
> [[Reader PDF]]
- **DOCX** — leitura feita com a biblioteca `python-docx`. 
> [[Reader DOCX]]
- **ODT** — leitura feita com a biblioteca `odfpy` (módulo `odf`). 
> [[Reader ODT]]
- **XML (DANFE/NFe)** — os arquivos XML de NFe seguem o schema fixo definido pela SEFAZ, com tags padronizadas. Hoje o XML **não é parseado**: o [[Reader XML]] apenas decodifica os bytes como texto (UTF-8, com fallback para Latin-1) e os campos são extraídos com Regex diretamente sobre as tags (ex.: `<chNFe>(\d{44})</chNFe>`). O parsing estruturado com `xml.etree.ElementTree` é o que o [[PT-RF 04|RF 04]] pede, mas ainda não foi implementado.
>  [[Reader XML]]

Para os documentos cujo conteúdo segue um padrão textual previsível — **Cartão CNPJ**, **NFe** e **CRLV** — a extração dos campos é feita por meio de [Regex](https://regexr.com/) aplicadas sobre o texto extraído de cada arquivo, independentemente da extensão de origem (PDF, DOCX ou ODT).

> [!warning] Laudos e contratos
> `LAUDO` e `CONTRATO` existem no enum e têm [[KeyWords (Protheus)|KeyWords]], então podem ser **classificados**, mas não têm [[Patterns (Protheus)|Patterns]]: o `DocumentExtractor` retorna `{}` para eles. A extração desses tipos ainda está planejada ([[PT-RF 02|RF 02]]).

**Referências de exemplo (estrutura de XML/DANFE):**
- [Exemplo de XML/DANFE](https://www.webdanfe.com.br/danfe/ExemploXml.html)
- [Exemplos de XML e DANFE de NF-e](https://www.devmedia.com.br/nf-e-exemplos-de-xml-e-danfe/21148)

## Fluxo Geral de Processamento

1. O usuário envia um documento por meio de uma requisição HTTP.
    
2. O [[Controller (Protheus)|Controller]] (`POST /document/extract`) recebe o arquivo e o entrega ao `ExtractDocumentUseCase` (camada Application), injetando o [[JSON Repository]]. O caso de uso orquestra as etapas abaixo.
    
3. O `DocumentExtensionDetector` identifica a extensão e o arquivo é gravado em um temporário.
    
4. A [[Factory (Protheus)|Factory]] devolve o reader da extensão, que extrai o conteúdo como texto.
    
5. O `DocumentTypeDetector` classifica o tipo (tags `<nfe>`/`<infnfe>` para XML, pontuação por [[KeyWords (Protheus)|KeyWords]] para os demais).
    
6. O `DocumentExtractor` aplica os [[Patterns (Protheus)|Patterns]] Regex do tipo detectado (inclusive no XML).
    
7. O caso de uso monta o `Document`, grava no log e o salva via `repository.save` ([[JSON Repository]] → `save_db` em `infrastructure/db/db.json`). O endpoint retorna o `dict` extraído.