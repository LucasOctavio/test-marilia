from fastapi import APIRouter, Header
from typing import Annotated
from models.auth import engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt as sha256
from models.auth import Usuario

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.get("/listar_dados")
async def dados(user : Annotated[str | None, Header()] = None):
    return {'user':user}


@router.get('/listar_nivel')
async def listar_nivel(nome: str, senha:str):
    session = sessionmaker(bind=engine)
    Session = session()
    if Session.query(Usuario).filter(Usuario.nome == nome).first():
        senhas = Usuario.verify(senha)
        if senhas:
            Session.query(Usuario).filter(Usuario.senha == nome).first()
        
    return None