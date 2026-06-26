from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# criaçao do app
app = FastAPI()

# configurando CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# carrega o env
load_dotenv()

# informaçao do banco
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# verifica se a porta é valida
if db_port and str(db_port).strip().lower() != "none":
    try:
        int(db_port)
        host_part = f"{db_host}:{db_port}"
    except (TypeError, ValueError):
        host_part = db_host
else:
    host_part = db_host

# url do banco postgresql
URL = f"postgresql+psycopg2://{db_user}:{db_password}@{host_part}/{db_name}"

# criaçao do engine
engine = create_engine(URL, echo=True)

# criaçao da Base
Base = declarative_base()

# importaçoes das rotas
from .routers.auth_router import auth_router
from .routers.usuario_router import usuario_router
from .routers.categoria_router import categoria_router
from .routers.pergunta_router import pergunta_router
from .routers.registro_router import registro_router

# inclui as rotas no app
app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(categoria_router)
app.include_router(pergunta_router)
app.include_router(registro_router)