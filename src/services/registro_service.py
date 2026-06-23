from ..models.model import Registro
from fastapi import HTTPException

def criar_registro(db, dados):
    """CREATE: Cria um registro de acerto/erro associado a user e categoria."""
    novo_registro = Registro(
        categoria_id=dados.categoria_id,
        user_id=dados.user_id,
        acerto_categoria=dados.acerto_categoria
    )
    
    try:
        db.add(novo_registro)
        db.commit()
        db.refresh(novo_registro)
        return {"mensagem": "Registro criado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Erro de integridade: Verifique se o user_id e a categoria_id existem."
        )

def listar_registros(db):
    """READ: Lista todos os registros cadastrados."""
    return db.query(Registro).all()

def buscar_registro_por_id(db, registro_id):
    """READ: Busca um registro pelo ID. Lança 404 se não for encontrado."""
    registro = db.query(Registro).filter(Registro.id == registro_id).first()
    if not registro:
        raise HTTPException(
            status_code=404, 
            detail=f"Registro com ID {registro_id} não encontrado."
        )
    return registro

def atualizar_registro(db, registro_id, dados):
    """UPDATE: Atualiza um registro existente.

    Recebe o schema `RegistroCreate` e retorna uma mensagem de confirmação.
    """
    registro = buscar_registro_por_id(db, registro_id)
    
    registro.categoria_id = dados.categoria_id
    registro.user_id = dados.user_id
    registro.acerto_categoria = dados.acerto_categoria
    
    try:
        db.commit()
        db.refresh(registro)
        return {"mensagem": "Registro atualizado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail="Erro de integridade ao atualizar: Verifique os IDs informados."
        )

def deletar_registro(db, registro_id):
    """DELETE: Remove um registro existente."""
    registro = buscar_registro_por_id(db, registro_id)
    
    db.delete(registro)
    db.commit()
    return {"mensagem": "Registro deletado com sucesso."}