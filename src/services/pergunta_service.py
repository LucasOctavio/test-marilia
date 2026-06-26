from fastapi import HTTPException
from src.models.model import Pergunta, Categoria

def criar_pergunta(pergunta_input, db):
    """CREATE: Cria uma nova pergunta.

    Recebe o schema `PerguntaCreate`, valida a categoria informada e salva no banco.
    Retorna somente uma mensagem de sucesso.
    """
    categoria_id = pergunta_input.categoria
    if categoria_id in (None, 0, ""):
        categoria_id = None
    elif categoria_id is not None:
        categoria_existe = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if not categoria_existe:
            raise HTTPException(status_code=400, detail=f"Não foi possível criar a pergunta: A categoria com ID {categoria_id} não existe.")

    nova_pergunta = Pergunta(
        pergunta=pergunta_input.pergunta,
        alternativas=pergunta_input.alternativas,
        resposta=pergunta_input.resposta,
        feedback=pergunta_input.feedback,
        categoria_id=categoria_id
    )
    
    try:
        db.add(nova_pergunta)
        db.commit()
        db.refresh(nova_pergunta)
        return {"mensagem": "Pergunta criada com sucesso.", "pergunta": nova_pergunta}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível criar a pergunta. Verifique os dados informados.") from exc


def listar_perguntas(db):
    """READ: Lista todas as perguntas cadastradas."""
    return db.query(Pergunta).all()


def buscar_pergunta(pergunta_id, db):
    """READ: Busca uma pergunta pelo ID. Lança 404 se não for encontrada."""
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(status_code=404, detail=f"Pergunta com ID {pergunta_id} não foi encontrada.")
    return pergunta


def atualizar_pergunta(pergunta_id, pergunta_input, db):
    """UPDATE: Atualiza os dados de uma pergunta completa.

    O schema `PerguntaCreate` define os campos que podem ser atualizados.
    """
    pergunta_banco = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta_banco:
        raise HTTPException(status_code=404, detail=f"Não foi possível atualizar: Pergunta com ID {pergunta_id} não existe.")

    categoria_id = pergunta_input.categoria
    if categoria_id in (None, 0, ""):
        categoria_id = None
    elif categoria_id is not None:
        categoria_existe = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if not categoria_existe:
            raise HTTPException(status_code=400, detail=f"Não foi possível atualizar: A categoria com ID {categoria_id} não existe.")

    try:
        pergunta_banco.pergunta = pergunta_input.pergunta
        pergunta_banco.alternativas = pergunta_input.alternativas
        pergunta_banco.resposta = pergunta_input.resposta
        pergunta_banco.feedback = pergunta_input.feedback
        pergunta_banco.categoria_id = categoria_id

        db.commit()
        db.refresh(pergunta_banco)
        return {"mensagem": "Pergunta atualizada com sucesso.", "pergunta": pergunta_banco}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível atualizar a pergunta. Verifique os dados informados.") from exc


def deletar_pergunta(pergunta_id, db):
    """DELETE: Remove uma pergunta pelo ID."""
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Pergunta com ID {pergunta_id} não existe.")
    
    try:
        db.delete(pergunta)
        db.commit()
        return {"mensagem": "Pergunta deletada com sucesso."}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível deletar a pergunta.") from exc