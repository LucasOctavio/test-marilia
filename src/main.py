from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(URL, echo=True)

class Base(DeclarativeBase):
    pass

from routers.auth_router import auth_router
from routers.usuario_router import usuario_router
from routers.categoria_router import categoria_router
from routers.pergunta_router import pergunta_router
from routers.registro_router import registro_router

app.include_router(auth_router)
app.include_router(usuario_router)
app.include_router(categoria_router)
app.include_router(pergunta_router)
app.include_router(registro_router)