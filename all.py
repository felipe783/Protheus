"""
deps.py
--------
Dependências (FastAPI `Depends`) para o sistema de upload e processamento de
documentos.

Cobre:
    RF01 - Upload de CRLV-e, Cartão CNPJ, DANFE/XML e laudos (PDF/XML/DOCX/ODT)
    RF03 - Classificação automática do tipo de documento (extensão + palavras-chave)
    RF04 - Extração de dados da NFe via parsing de XML, com fallback OCR+regex para DANFE
    RF05 - Extração de dados do CRLV-e e Cartão CNPJ via texto/OCR + regex posicional
    RF09 - Extração de multas, prazos, valores e partes do contrato (regex + NER)

Persistência: arquivo JSON simples em disco (`db.json`). A classe `JSONRepository`
foi pensada para manter a mesma interface pública quando isso for migrado para
SQL (SQLAlchemy) e quando usuários forem introduzidos no sistema.

Dependências externas (ver requirements.txt):
    fastapi, python-multipart, pdfplumber, python-docx, odfpy,
    pytesseract, pdf2image, Pillow, spacy (+ modelo pt_core_news_sm)

Requer também, no sistema operacional: tesseract-ocr e poppler-utils
(usados por pytesseract/pdf2image para fazer OCR).
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unicodedata
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from xml.etree import ElementTree as ET

from fastapi import Depends, HTTPException, UploadFile, status

# --- Extração de texto -------------------------------------------------------
import pdfplumber
import docx  # python-docx
from odf.opendocument import load as odf_load
from odf.text import P as OdfParagraph

# --- OCR ----------------------------------------------------------------------
import pytesseract
from pdf2image import convert_from_path

# --- NER (opcional) -------------------------------------------------------------
try:
    import spacy

    _NLP = spacy.load("pt_core_news_sm")
except Exception:
    # Se o spaCy ou o modelo PT não estiverem instalados, a extração de partes
    # do contrato continua funcionando apenas com regex (RF09), sem o reforço de NER.
    _NLP = None


# =============================================================================
# Constantes e tipos
# =============================================================================

class TipoDocumento(str, Enum):
    CRLV_E = "crlv_e"
    CARTAO_CNPJ = "cartao_cnpj"
    DANFE_XML = "danfe_xml"
    LAUDO = "laudo"
    CONTRATO = "contrato"
    DESCONHECIDO = "desconhecido"


EXTENSOES_PERMITIDAS = {".pdf", ".xml", ".docx", ".odt"}
MAX_TAMANHO_MB = 20

# RF03 - palavras-chave usadas na classificação automática do documento
PALAVRAS_CHAVE: dict[TipoDocumento, list[str]] = {
    TipoDocumento.CRLV_E: [
        "crlv", "certificado de registro e licenciamento", "renavam",
        "licenciamento de veiculo", "exercicio",
    ],
    TipoDocumento.CARTAO_CNPJ: [
        "cartao cnpj", "comprovante de inscricao", "cadastro nacional da pessoa juridica",
        "situacao cadastral", "receita federal",
    ],
    TipoDocumento.DANFE_XML: [
        "danfe", "nota fiscal eletronica", "nfe", "chave de acesso",
        "protocolo de autorizacao", "documento auxiliar da nota fiscal",
    ],
    TipoDocumento.LAUDO: [
        "laudo", "laboratorio", "analise laboratorial", "resultado de exame", "amostra",
    ],
    TipoDocumento.CONTRATO: [
        "contrato", "contratante", "contratada", "clausula", "rescisao", "multa",
        "partes contratantes",
    ],
}


# =============================================================================
# RF — "Banco de dados" em JSON (substituível por SQL no futuro)
# =============================================================================

DB_PATH = Path(os.getenv("JSON_DB_PATH", "db.json"))


def _carregar_db() -> dict:
    if not DB_PATH.exists():
        return {"documentos": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"documentos": []}


def _salvar_db(data: dict) -> None:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


class JSONRepository:
    """
    Repositório simples baseado em arquivo JSON.

    Interface pensada para ser trocada por um repositório SQL (ex.: SQLAlchemy)
    no futuro sem precisar mudar quem consome (`add_documento`, `get_documento`,
    `list_documentos`, `update_documento`).
    """

    def __init__(self) -> None:
        self._data = _carregar_db()

    def add_documento(self, documento: dict) -> dict:
        documento["id"] = documento.get("id") or str(uuid.uuid4())
        documento["criado_em"] = documento.get("criado_em") or datetime.utcnow().isoformat()
        self._data["documentos"].append(documento)
        _salvar_db(self._data)
        return documento

    def get_documento(self, doc_id: str) -> Optional[dict]:
        return next((d for d in self._data["documentos"] if d["id"] == doc_id), None)

    def list_documentos(self) -> list[dict]:
        return self._data["documentos"]

    def update_documento(self, doc_id: str, **campos: Any) -> Optional[dict]:
        doc = self.get_documento(doc_id)
        if doc:
            doc.update(campos)
            _salvar_db(self._data)
        return doc


def get_repository() -> JSONRepository:
    """Dependência FastAPI: injeta o repositório de documentos (JSON por enquanto)."""
    return JSONRepository()


# =============================================================================
# RF01 — Upload de documentos
# =============================================================================

async def validar_upload(file: UploadFile) -> UploadFile:
    """
    RF01 - Garante que o arquivo enviado tem extensão suportada
    (pdf, xml, docx, odt) e respeita o tamanho máximo permitido.
    """
    extensao = Path(file.filename or "").suffix.lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Extensão '{extensao}' não suportada. Use: {', '.join(sorted(EXTENSOES_PERMITIDAS))}",
        )

    conteudo = await file.read()
    tamanho_mb = len(conteudo) / (1024 * 1024)
    if tamanho_mb > MAX_TAMANHO_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo excede o limite de {MAX_TAMANHO_MB}MB.",
        )

    await file.seek(0)  # devolve o cursor pro início, pra próxima leitura
    return file


async def salvar_arquivo_temp(file: UploadFile = Depends(validar_upload)) -> Path:
    """
    Salva o upload em um arquivo temporário em disco e devolve o Path.
    Necessário porque as libs de PDF/OCR (pdfplumber, pdf2image) trabalham
    melhor com caminho de arquivo do que com stream em memória.
    """
    extensao = Path(file.filename).suffix.lower()
    tmp_dir = Path(tempfile.gettempdir()) / "uploads_documentos"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    destino = tmp_dir / f"{uuid.uuid4()}{extensao}"

    with open(destino, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return destino


# =============================================================================
# Extração de texto (base para RF03, RF05 e RF09)
# =============================================================================

def _ocr_pdf(caminho: Path) -> str:
    """OCR de PDF escaneado/fotografado, página por página, via pytesseract."""
    texto = ""
    try:
        imagens = convert_from_path(str(caminho))
        for imagem in imagens:
            texto += pytesseract.image_to_string(imagem, lang="por") + "\n"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Falha ao executar OCR no documento: {e}",
        )
    return texto


def extrair_texto(caminho: Path) -> str:
    """
    Extrai texto bruto de PDF, DOCX, ODT ou XML.

    Usado pela classificação (RF03) e como base para extração de campos
    (RF05/RF09) quando não há parsing estruturado disponível (RF04 trata o
    caso do XML de NFe separadamente).

    Para PDF, tenta extração de texto nativo primeiro; se vier vazio
    (documento escaneado/fotografado), cai para OCR.
    """
    extensao = caminho.suffix.lower()

    if extensao == ".xml":
        return caminho.read_text(encoding="utf-8", errors="ignore")

    if extensao == ".docx":
        documento = docx.Document(str(caminho))
        return "\n".join(p.text for p in documento.paragraphs)

    if extensao == ".odt":
        odt = odf_load(str(caminho))
        paragrafos = odt.getElementsByType(OdfParagraph)
        return "\n".join(str(p) for p in paragrafos)

    if extensao == ".pdf":
        texto = ""
        with pdfplumber.open(str(caminho)) as pdf:
            for pagina in pdf.pages:
                texto += (pagina.extract_text() or "") + "\n"

        if texto.strip():
            return texto

        return _ocr_pdf(caminho)  # RF04/RF05 - fallback OCR

    return ""


async def get_texto_extraido(caminho: Path = Depends(salvar_arquivo_temp)) -> tuple[Path, str]:
    """Dependência que devolve (caminho_do_arquivo, texto_extraido)."""
    texto = extrair_texto(caminho)
    return caminho, texto


# =============================================================================
# RF03 — Classificação automática do tipo de documento
# =============================================================================

def _normalizar(texto: str) -> str:
    """minúsculas + remove acentos, pra comparar palavras-chave sem depender de acentuação."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def classificar_documento(caminho: Path, texto: str) -> TipoDocumento:
    """
    RF03 - Classifica o documento combinando:
      1) Extensão do arquivo (sinal forte: .xml costuma ser DANFE/NFe)
      2) Contagem de palavras-chave encontradas no texto extraído

    O tipo com maior pontuação de palavras-chave vence; em caso de nenhuma
    palavra-chave reconhecida, devolve DESCONHECIDO.
    """
    extensao = caminho.suffix.lower()
    texto_norm = _normalizar(texto)

    if extensao == ".xml" and ("infnfe" in texto_norm or "<nfe" in texto_norm):
        return TipoDocumento.DANFE_XML

    pontuacao: dict[TipoDocumento, int] = {tipo: 0 for tipo in PALAVRAS_CHAVE}
    for tipo, palavras in PALAVRAS_CHAVE.items():
        for palavra in palavras:
            if _normalizar(palavra) in texto_norm:
                pontuacao[tipo] += 1

    tipo_vencedor = max(pontuacao, key=pontuacao.get)
    if pontuacao[tipo_vencedor] == 0:
        return TipoDocumento.DESCONHECIDO

    return tipo_vencedor


async def get_tipo_documento(
    dados: tuple[Path, str] = Depends(get_texto_extraido),
) -> dict[str, Any]:
    """
    Dependência principal: devolve {"caminho", "texto", "tipo"}, pronta para
    ser injetada nas rotas de upload/processamento e usada para rotear o
    arquivo para a extração correta (RF04/RF05/RF09).
    """
    caminho, texto = dados
    tipo = classificar_documento(caminho, texto)
    return {"caminho": caminho, "texto": texto, "tipo": tipo}


# =============================================================================
# RF04 — Extração de dados da NFe (XML/DANFE)
# =============================================================================

def _remover_namespaces(elemento: ET.Element) -> ET.Element:
    """Remove namespaces das tags (ex.: '{http://...}ide' -> 'ide'), simplificando os XPaths."""
    for el in elemento.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return elemento


def extrair_dados_nfe_xml(caminho: Path) -> dict[str, Any]:
    """
    RF04 - Extrai campos da NFe via parsing direto do XML, lendo as tags
    <ide>, <dest>, <det> e <total> conforme o layout oficial da NF-e (SEFAZ).
    """
    raiz = _remover_namespaces(ET.parse(str(caminho)).getroot())
    inf_nfe = raiz.find(".//infNFe")
    if inf_nfe is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="XML não contém a tag <infNFe> esperada de uma NFe.",
        )

    def txt(no: Optional[ET.Element], tag: str) -> Optional[str]:
        if no is None:
            return None
        el = no.find(tag)
        return el.text.strip() if el is not None and el.text else None

    ide = inf_nfe.find("ide")
    dest = inf_nfe.find("dest")
    total = inf_nfe.find("total/ICMSTot")

    itens = []
    for det in inf_nfe.findall("det"):
        prod = det.find("prod")
        itens.append(
            {
                "codigo": txt(prod, "cProd"),
                "descricao": txt(prod, "xProd"),
                "ncm": txt(prod, "NCM"),
                "quantidade": txt(prod, "qCom"),
                "valor_unitario": txt(prod, "vUnCom"),
                "valor_total": txt(prod, "vProd"),
            }
        )

    chave_acesso = inf_nfe.attrib.get("Id", "").replace("NFe", "") or None

    return {
        "chave_acesso": chave_acesso,
        "numero_nf": txt(ide, "nNF"),
        "serie": txt(ide, "serie"),
        "data_emissao": txt(ide, "dhEmi") or txt(ide, "dEmi"),
        "destinatario_nome": txt(dest, "xNome"),
        "destinatario_cnpj_cpf": txt(dest, "CNPJ") or txt(dest, "CPF"),
        "itens": itens,
        "valor_total_produtos": txt(total, "vProd"),
        "valor_total_nota": txt(total, "vNF"),
        "origem_extracao": "xml",
    }


_REGEX_DANFE = {
    "chave_acesso": re.compile(r"(\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{2})"),
    "numero_nf": re.compile(r"N[º°o]\.?\s*[:\-]?\s*(\d{1,9})", re.IGNORECASE),
    "serie": re.compile(r"S[ée]rie\s*[:\-]?\s*(\d{1,3})", re.IGNORECASE),
    "data_emissao": re.compile(r"(?:DATA\s+DA\s+EMISS[ÃA]O|EMISS[ÃA]O)\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE),
    "destinatario_cnpj_cpf": re.compile(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{3}\.\d{3}\.\d{3}-\d{2})"),
    "valor_total_nota": re.compile(r"VALOR\s+TOTAL\s+DA\s+NOTA\s*[:\-]?\s*R?\$?\s*([\d\.,]+)", re.IGNORECASE),
}


def extrair_dados_danfe_ocr(texto: str) -> dict[str, Any]:
    """
    RF04 - Fallback: extrai os mesmos campos da NFe a partir de texto obtido
    via OCR/extração de texto do DANFE impresso ou escaneado, usando regex
    baseadas no layout padrão do DANFE. (Itens detalhados exigiriam OCR
    posicional/tabular mais robusto e ficam fora deste fallback simples.)
    """
    dados: dict[str, Any] = {}
    for campo, regex in _REGEX_DANFE.items():
        m = regex.search(texto)
        dados[campo] = m.group(1).strip() if m else None
    dados["itens"] = []
    dados["origem_extracao"] = "ocr"
    return dados


async def get_dados_nfe(contexto: dict[str, Any] = Depends(get_tipo_documento)) -> dict[str, Any]:
    """
    Dependência da rota de NFe/DANFE (RF04).
    Usa parsing direto se for XML; senão aplica regex sobre o texto
    nativo/OCR extraído do PDF (DANFE impresso ou escaneado).
    """
    if contexto["tipo"] != TipoDocumento.DANFE_XML:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Documento classificado como '{contexto['tipo'].value}', não é DANFE/NFe.",
        )

    caminho: Path = contexto["caminho"]
    if caminho.suffix.lower() == ".xml":
        dados = extrair_dados_nfe_xml(caminho)
    else:
        dados = extrair_dados_danfe_ocr(contexto["texto"])

    return {**contexto, "dados_extraidos": dados}


# =============================================================================
# RF05 — Extração de dados do CRLV-e e Cartão CNPJ
# =============================================================================

_REGEX_CRLV = {
    "renavam": re.compile(r"RENAVAM\s*[:\-]?\s*(\d{9,11})", re.IGNORECASE),
    "placa": re.compile(r"PLACA\s*[:\-]?\s*([A-Z]{3}[\-]?\d[A-Z0-9]\d{2})", re.IGNORECASE),
    "chassi": re.compile(r"CHASSI\s*[:\-]?\s*([A-Z0-9]{17})", re.IGNORECASE),
    "marca_modelo": re.compile(r"MARCA\s*/?\s*MODELO\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "ano_fabricacao": re.compile(r"ANO\s*FAB(?:RICA[ÇC][ÃA]O)?\s*[:\-]?\s*(\d{4})", re.IGNORECASE),
    "ano_modelo": re.compile(r"ANO\s*MOD(?:ELO)?\s*[:\-]?\s*(\d{4})", re.IGNORECASE),
    "cor": re.compile(r"COR\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "proprietario": re.compile(r"PROPRIET[ÁA]RIO\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "municipio_uf": re.compile(r"MUNIC[ÍI]PIO\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "categoria": re.compile(r"CATEGORIA\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
}


def extrair_dados_crlv(texto: str) -> dict[str, Any]:
    """
    RF05 - Extrai campos do CRLV-e a partir do texto (nativo ou OCR),
    aplicando regex posicionais baseadas no layout oficial fixo do
    documento (Detran/Renavam).
    """
    dados = {}
    for campo, regex in _REGEX_CRLV.items():
        m = regex.search(texto)
        dados[campo] = m.group(1).strip() if m else None
    return dados


_REGEX_CNPJ_CARTAO = {
    "cnpj": re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"),
    "razao_social": re.compile(r"NOME\s+EMPRESARIAL\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "nome_fantasia": re.compile(r"NOME\s+FANTASIA\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "data_abertura": re.compile(r"DATA\s+DE\s+ABERTURA\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE),
    "situacao_cadastral": re.compile(r"SITUA[ÇC][ÃA]O\s+CADASTRAL\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "atividade_principal": re.compile(r"ATIVIDADE\s+ECON[ÔO]MICA\s+PRINCIPAL\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "endereco": re.compile(r"LOGRADOURO\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "municipio": re.compile(r"MUNIC[ÍI]PIO\s*[:\-]?\s*([^\n]+)", re.IGNORECASE),
    "uf": re.compile(r"\bUF\s*[:\-]?\s*([A-Z]{2})\b"),
}


def extrair_dados_cartao_cnpj(texto: str) -> dict[str, Any]:
    """
    RF05 - Extrai campos do Cartão CNPJ a partir do texto (nativo ou OCR),
    aplicando regex posicionais baseadas no layout oficial da Receita Federal.
    """
    dados = {}
    for campo, regex in _REGEX_CNPJ_CARTAO.items():
        m = regex.search(texto)
        if not m:
            dados[campo] = None
        elif m.groups():
            dados[campo] = m.group(1).strip()
        else:
            dados[campo] = m.group(0).strip()
    return dados


async def get_dados_crlv_ou_cnpj(
    contexto: dict[str, Any] = Depends(get_tipo_documento),
) -> dict[str, Any]:
    """
    Dependência da rota de CRLV-e / Cartão CNPJ (RF05). Usa o texto já
    extraído (nativo ou OCR) e aplica o conjunto de regex correspondente
    ao tipo classificado em RF03.
    """
    tipo = contexto["tipo"]
    texto = contexto["texto"]

    if tipo == TipoDocumento.CRLV_E:
        dados = extrair_dados_crlv(texto)
    elif tipo == TipoDocumento.CARTAO_CNPJ:
        dados = extrair_dados_cartao_cnpj(texto)
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Documento classificado como '{tipo.value}', não é CRLV-e nem Cartão CNPJ.",
        )

    return {**contexto, "dados_extraidos": dados}


# =============================================================================
# RF09 — Extração de entidades do contrato
# =============================================================================

_REGEX_CONTRATO = {
    "valores_reais": re.compile(r"R\$\s?[\d\.]*\d+,\d{2}"),
    "percentuais": re.compile(r"\d{1,3}(?:,\d+)?\s?%"),
    "prazos_dias": re.compile(r"\d{1,4}\s*\(?\s*(?:dias|dia)\b", re.IGNORECASE),
    "multas": re.compile(
        r"multa[^.\n]{0,120}?(?:R\$\s?[\d\.]*\d+,\d{2}|\d{1,3}(?:,\d+)?\s?%)",
        re.IGNORECASE,
    ),
}


def extrair_valores_e_prazos(texto: str) -> dict[str, list[str]]:
    """
    RF09 - Extrai, via expressões regulares, valores em reais, percentuais,
    prazos em dias e trechos que mencionam multas.
    """
    return {
        "valores_reais": _REGEX_CONTRATO["valores_reais"].findall(texto),
        "percentuais": _REGEX_CONTRATO["percentuais"].findall(texto),
        "prazos_dias": _REGEX_CONTRATO["prazos_dias"].findall(texto),
        "trechos_multa": _REGEX_CONTRATO["multas"].findall(texto),
    }


_ROTULOS_PARTES = ("contratante", "contratada", "locador", "locatário", "locataria", "credor", "devedor")


def extrair_partes_responsaveis(texto: str) -> list[dict[str, str]]:
    """
    RF09 - Identifica as partes responsáveis pelo contrato combinando:
      1) Regex sobre rótulos típicos de contrato (CONTRATANTE:, CONTRATADA:, etc.)
      2) NER (spaCy, modelo pt_core_news_sm) para localizar entidades do tipo
         PESSOA (PER) e ORGANIZAÇÃO (ORG), cobrindo os casos mais variáveis em
         que o nome não aparece logo após um rótulo fixo.
    """
    partes: list[dict[str, str]] = []

    # 1) Regex pelos rótulos contratuais
    for rotulo in _ROTULOS_PARTES:
        m = re.search(rf"{rotulo}\s*[:\-]?\s*([^\n,;]+)", texto, re.IGNORECASE)
        if m:
            partes.append({"papel": rotulo.upper(), "nome": m.group(1).strip(), "origem": "regex"})

    # 2) NER para reforçar/complementar nomes de pessoas e empresas citados no texto
    if _NLP is not None:
        doc = _NLP(texto[:100_000])  # limite defensivo para contratos muito longos
        nomes_ja_encontrados = {p["nome"].lower() for p in partes}
        for ent in doc.ents:
            if ent.label_ in ("PER", "ORG") and ent.text.lower() not in nomes_ja_encontrados:
                partes.append({"papel": ent.label_, "nome": ent.text.strip(), "origem": "ner"})
                nomes_ja_encontrados.add(ent.text.lower())

    return partes


def extrair_entidades_contrato(texto: str) -> dict[str, Any]:
    """RF09 - Consolida a extração de multas, prazos, valores e partes do contrato."""
    return {
        **extrair_valores_e_prazos(texto),
        "partes_responsaveis": extrair_partes_responsaveis(texto),
    }


async def get_dados_contrato(contexto: dict[str, Any] = Depends(get_tipo_documento)) -> dict[str, Any]:
    """Dependência da rota de contratos (RF09)."""
    if contexto["tipo"] != TipoDocumento.CONTRATO:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Documento classificado como '{contexto['tipo'].value}', não é um contrato.",
        )
    dados = extrair_entidades_contrato(contexto["texto"])
    return {**contexto, "dados_extraidos": dados}


# =============================================================================
# Laudos — sem regras de extração de campo definidas ainda (apenas RF03 cobre)
# =============================================================================

async def get_dados_laudo(contexto: dict[str, Any] = Depends(get_tipo_documento)) -> dict[str, Any]:
    """
    Dependência da rota de laudos laboratoriais. Nenhum RF definiu ainda
    regras específicas de extração de campos para laudos — por ora devolve
    o texto extraído, podendo evoluir para regex/NER quando isso for definido.
    """
    if contexto["tipo"] != TipoDocumento.LAUDO:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Documento classificado como '{contexto['tipo'].value}', não é um laudo.",
        )
    return contexto


# =============================================================================
# Dependência "roteadora" — uma única rota genérica de upload (opcional)
# =============================================================================

async def processar_e_salvar(
    contexto: dict[str, Any] = Depends(get_tipo_documento),
    repo: JSONRepository = Depends(get_repository),
) -> dict[str, Any]:
    """
    A partir do tipo classificado (RF03), aplica a extração correta
    (RF04/RF05/RF09) e persiste o resultado no JSON. Útil para uma única
    rota de upload genérica que processa qualquer um dos tipos suportados,
    em vez de uma rota por tipo de documento.
    """
    tipo = contexto["tipo"]
    caminho: Path = contexto["caminho"]
    texto = contexto["texto"]

    if tipo == TipoDocumento.DANFE_XML:
        dados = (
            extrair_dados_nfe_xml(caminho)
            if caminho.suffix.lower() == ".xml"
            else extrair_dados_danfe_ocr(texto)
        )
    elif tipo == TipoDocumento.CRLV_E:
        dados = extrair_dados_crlv(texto)
    elif tipo == TipoDocumento.CARTAO_CNPJ:
        dados = extrair_dados_cartao_cnpj(texto)
    elif tipo == TipoDocumento.CONTRATO:
        dados = extrair_entidades_contrato(texto)
    elif tipo == TipoDocumento.LAUDO:
        dados = {"texto_extraido": texto}
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível identificar o tipo do documento enviado.",
        )

    registro = repo.add_documento(
        {
            "nome_arquivo": caminho.name,
            "tipo": tipo.value,
            "dados_extraidos": dados,
        }
    )

    return registro