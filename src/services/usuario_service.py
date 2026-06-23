from sqlalchemy.orm import Session
from ..models.model import Usuario
from fastapi import HTTPException


# CREATE: Cria um novo usuário a partir dos dados enviados pelo router.
#  - Validações de unicidade são tratadas pela tentativa de commit no banco.
#  - Em caso de sucesso retorna um dicionário com `mensagem`.
def criar_usuario(usuario_input, db):
    """Cria um novo usuário e retorna mensagem de confirmação."""

    novo_usuario = Usuario(
        nome=usuario_input.nome,
        senha=usuario_input.senha,
        nivel=getattr(usuario_input, "nivel", 0),
    )
    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {"mensagem": "Usuário criado com sucesso."}
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"O nome de usuário '{usuario_input.nome}' já está em uso.")

def listar_usuarios(db):
    """READ: Lista todos os usuários."""
    return db.query(Usuario).all()

def buscar_usuario(usuario_id, db):
    """READ: Busca um usuário pelo ID. Lança 404 se não encontrar."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuário com ID {usuario_id} não foi encontrado.")
    return usuario

def atualizar_progresso(usuario_id, dados, db):
    """UPDATE: Atualiza `acerto_total` e `erro_total` do usuário.

    - Recebe o schema `UsuarioUpdateProgresso` com os campos atualizáveis.
    - Retorna mensagem de confirmação ao finalizar.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail=f"Não foi possível atualizar: Usuário com ID {usuario_id} não existe.")

    usuario.acerto_total = dados.acerto_total
    usuario.erro_total = dados.erro_total

    db.commit()
    db.refresh(usuario)
    return {"mensagem": "Progresso atualizado com sucesso."}

def deletar_usuario(usuario_id, db):
    """DELETE: Remove um usuário.

    - Em caso de sucesso retorna um dicionário com `mensagem`.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail=f"Não foi possível deletar: Usuário com ID {usuario_id} não existe.")

    db.delete(usuario)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso."}