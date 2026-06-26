from fastapi import APIRouter, Depends
from src.services.pergunta_service import criar_pergunta, listar_perguntas, buscar_pergunta, atualizar_pergunta, deletar_pergunta
from src.schemas.pergunta_schema import PerguntaCreate, PerguntaResponse, PerguntaMensagemResponse
from src.dependencies import get_session

pergunta_router = APIRouter(prefix="/pergunta", tags=["pergunta"])

@pergunta_router.get("/read", response_model=list[PerguntaResponse])
def listar_perguntas_endpoint(db = Depends(get_session)):
    return listar_perguntas(db)

@pergunta_router.get("/read/{pergunta_id}", response_model=PerguntaResponse)
def buscar_pergunta_endpoint(pergunta_id: int, db = Depends(get_session)):
    return buscar_pergunta(pergunta_id, db)

@pergunta_router.post("/create", response_model=PerguntaMensagemResponse, status_code=201)
def criar_pergunta_endpoint(pergunta_input: PerguntaCreate, db = Depends(get_session)):
    return criar_pergunta(pergunta_input, db)

@pergunta_router.put("/update/{pergunta_id}", response_model=PerguntaMensagemResponse)
def atualizar_pergunta_endpoint(pergunta_id: int, pergunta_input: PerguntaCreate, db = Depends(get_session)):
    return atualizar_pergunta(pergunta_id, pergunta_input, db)

@pergunta_router.delete("/delete/{pergunta_id}", response_model=PerguntaResponse)
def deletar_pergunta_endpoint(pergunta_id: int, db = Depends(get_session)):
    return deletar_pergunta(pergunta_id, db)