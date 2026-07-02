# source .venv/bin/activate
# http://127.0.0.1:8000/docs

# Terminal 1
# cd FrontEnd
# python -m http.server 5500
# http://localhost:5500/

# Terminal 2
# python -m uvicorn api.main:app --reload

from fastapi import FastAPI
from api.routers.ControllerDocument import documentController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(documentController)