from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services.categoria_service import criar_categoria, listar_categorias, buscar_categoria, atualizar_categoria, deletar_categoria
from ..schemas.categoria_schema import CategoriaCreate, CategoriaResponse
from ..dependencies import get_session

categoria_router = APIRouter(prefix="/categoria", tags=["Categoria"])

@categoria_router.get("/read", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_session)):
    return listar_categorias(db)

@categoria_router.get("/read/{categoria_id}", response_model=CategoriaResponse)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_session)):
    return buscar_categoria(categoria_id, db)

@categoria_router.post("/create", response_model=CategoriaResponse, status_code=201)
def criar_categoria(categoria_input: CategoriaCreate, db: Session = Depends(get_session)):
    return criar_categoria(categoria_input, db)

@categoria_router.put("/update/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, categoria_input: CategoriaCreate, db: Session = Depends(get_session)):
    return atualizar_categoria(categoria_id, categoria_input, db)

@categoria_router.delete("/delete/{categoria_id}", status_code=204)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_session)):
    return deletar_categoria(categoria_id, db)