from fastapi import HTTPException
from ..models.model import Categoria


def criar_categoria(categoria_input, db):
    """CREATE: Cria uma nova categoria.

    Recebe o schema `CategoriaCreate`, valida a existência e salva no banco.
    Retorna uma mensagem de sucesso.
    """
    nova_categoria = Categoria(nome=categoria_input.nome)
    try:
        db.add(nova_categoria)
        db.commit()
        db.refresh(nova_categoria)
        return {"mensagem": "Categoria criada com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"A categoria '{categoria_input.nome}' já está cadastrada.")


def listar_categorias(db):
    """READ: Lista todas as categorias cadastradas."""
    return db.query(Categoria).all()


def buscar_categoria(categoria_id, db):
    """READ: Busca uma categoria pelo ID. Lança 404 se não existir."""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Categoria com ID {categoria_id} não foi encontrada.")
    return categoria


def atualizar_categoria(categoria_id, categoria_input, db):
    """UPDATE: Atualiza o nome de uma categoria existente.

    Recebe o schema `CategoriaCreate` para os dados de entrada e retorna mensagem.
    """
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Não foi possível atualizar: Categoria com ID {categoria_id} não existe.")
    
    try:
        categoria.nome = categoria_input.nome
        db.commit()
        db.refresh(categoria)
        return {"mensagem": "Categoria atualizada com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Não foi possível atualizar: O nome '{categoria_input.nome}' já está em uso por outra categoria.")


def deletar_categoria(categoria_id, db):
    """DELETE: Remove uma categoria pelo ID."""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Categoria com ID {categoria_id} não existe.")
    
    db.delete(categoria)
    db.commit()
    return {"mensagem": "Categoria deletada com sucesso."}