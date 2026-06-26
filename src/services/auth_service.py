from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.model import Usuario


def login(db, credenciais):
    """Autentica um usuário usando as credenciais fornecidas.

    Recebe o schema UsuarioLogin, busca o usuário no banco e compara a senha.
    Retorna uma mensagem de sucesso ou levanta uma HTTPException em caso de erro.
    """
    usuario = db.query(Usuario).filter(Usuario.nome == credenciais.nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if not usuario.verify(credenciais.senha):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
        
    return {"mensagem": "Usuário autenticado com sucesso!"}


def criar_conta(db, dados):
    """Cria uma nova conta de usuário.

    Recebe o schema UsuarioCreate, verifica se o nome já existe e cria o registro.
    Retorna uma mensagem de confirmação após salvar no banco.
    """
    usuario = db.query(Usuario).filter(Usuario.nome == dados.nome).first()
    
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")        
    
    novo_user = Usuario(nome=dados.nome, senha=dados.senha)
    novo_user.criptografar(dados.senha)
    
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    
    return {"mensagem": "Conta criada com sucesso."}


def dados(db, nome):
    """Retorna os dados do usuário solicitado pelo nome.

    Busca o usuário no banco e retorna o objeto para o router serializar.
    """
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario


def listar_nivel(db, nome):
    """Retorna o nível do usuário.

    Busca o usuário pelo nome e retorna uma mensagem com o nível atual.
    """
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    return {"mensagem": f"Nível do usuário {usuario.nome}", "nivel": usuario.nivel}


def deletar_user(db, nome):
    """Deleta o usuário identificado pelo nome.

    Remove o registro do banco e retorna uma mensagem de confirmação.
    """
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão")
        
    db.delete(usuario)
    db.commit()
    return {"mensagem": "Usuário deletado com sucesso"}