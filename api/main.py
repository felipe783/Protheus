# https://www.webdanfe.com.br/danfe/ExemploXml.html
# Site com exemplo de xml
# python -m uvicorn api.main:app --reload
# source .venv/bin/activate
# http://127.0.0.1:8000/docs

from fastapi import FastAPI
from api.routers.ControllerDocument import documentController

app = FastAPI()

app.include_router(documentController)