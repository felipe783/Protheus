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
- **XML (DANFE/NFe)** — os arquivos XML de NFe seguem o schema fixo definido pela SEFAZ, com tags padronizadas. A leitura é feita com a biblioteca padrão `xml.etree.ElementTree`, sem necessidade de bibliotecas externas como `lxml`. 
>  [[Reader XML]]

Para os documentos cujo conteúdo segue um padrão textual previsível — **Cartão CNPJ**, **NFe** e **CRLV** — a extração dos campos é feita por meio de [Regex](https://regexr.com/) aplicadas sobre o texto extraído de cada arquivo, independentemente da extensão de origem (PDF, DOCX ou ODT).

**Referências de exemplo (estrutura de XML/DANFE):**
- [Exemplo de XML/DANFE](https://www.webdanfe.com.br/danfe/ExemploXml.html)
- [Exemplos de XML e DANFE de NF-e](https://www.devmedia.com.br/nf-e-exemplos-de-xml-e-danfe/21148)