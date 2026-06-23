from fastapi import HTTPException
from ..models.model import Pergunta, Categoria

def criar_pergunta(pergunta_input, db):
    """CREATE: Cria uma nova pergunta.

    Recebe o schema `PerguntaCreate`, valida a categoria informada e salva no banco.
    Retorna somente uma mensagem de sucesso.
    """
    # Validação da Chave Estrangeira (Categoria)
    if pergunta_input.categoria:
        categoria_existe = db.query(Categoria).filter(Categoria.id == pergunta_input.categoria).first()
        if not categoria_existe:
            raise HTTPException(status_code=400, detail=f"Não foi possível criar a pergunta: A categoria com ID {pergunta_input.categoria} não existe.")

    nova_pergunta = Pergunta(
        pergunta=pergunta_input.pergunta,
        alternativas=pergunta_input.alternativas,
        resposta=pergunta_input.resposta,
        feedback=pergunta_input.feedback,
        categoria_id=pergunta_input.categoria
    )
    
    db.add(nova_pergunta)
    db.commit()
    db.refresh(nova_pergunta)
    return {"mensagem": "Pergunta criada com sucesso."}


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
    
    if pergunta_input.categoria:
        categoria_existe = db.query(Categoria).filter(Categoria.id == pergunta_input.categoria).first()
        if not categoria_existe:
            raise HTTPException(status_code=400, detail=f"Não foi possível atualizar: A categoria com ID {pergunta_input.categoria} não existe.")

    pergunta_banco.pergunta = pergunta_input.pergunta
    pergunta_banco.alternativas = pergunta_input.alternativas
    pergunta_banco.resposta = pergunta_input.resposta
    pergunta_banco.feedback = pergunta_input.feedback
    pergunta_banco.categoria_id = pergunta_input.categoria

    db.commit()
    db.refresh(pergunta_banco)
    return {"mensagem": "Pergunta atualizada com sucesso."}


def deletar_pergunta(pergunta_id, db):
    """DELETE: Remove uma pergunta pelo ID."""
    pergunta = db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()
    if not pergunta:
        raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Pergunta com ID {pergunta_id} não existe.")
    
    db.delete(pergunta)
    db.commit()
    return {"mensagem": "Pergunta deletada com sucesso."}