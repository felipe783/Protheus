# Extração de Dados da NF-e (XML/DANFE)

O sistema deve extrair os campos da nota fiscal eletrônica por meio do parsing direto do XML (tags como `<ide>`, `<dest>`, `<det>` e `<total>`), quando o arquivo XML estiver disponível. Quando apenas o DANFE (impresso ou digitalizado) estiver disponível, a extração deve ser feita via leitura de texto do PDF ou OCR, no caso de documentos escaneados.