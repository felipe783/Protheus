from enum import Enum
from typing import Generator, Optional
from Protheus.app.core.path_config import settings
from Protheus.app.infrastructure.db.session import SessionLocal
from Protheus.app.domain.models.user import User
from Protheus.app.application.services.ocr_service import OCRService
from Protheus.app.application.services.document_classifier import DocumentClassifierService
from Protheus.app.application.services.nfe_parser import NFeParserService
from Protheus.app.application.services.embedding_service import EmbeddingService
from Protheus.app.application.services.ner_service import NERService
from Protheus.app.application.services.storage_service import StorageService
from __future__ import annotations
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from xml.etree import ElementTree as ET
import json
import os
import re
import shutil
import tempfile
import unicodedata
import uuid
from app.core.path_config import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Caminho JSON
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def _get_db() -> dict:
    if not DB_PATH.exists():
        return {"documents": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"documents": []}