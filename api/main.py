# https://www.webdanfe.com.br/danfe/ExemploXml.html
# Site com exemplo de xml
# python -m uvicorn api.main:app --reload

from fastapi import FastAPI
from api.routers.ControllerDocument import documentController

app = FastAPI()

app.include_router(documentController)