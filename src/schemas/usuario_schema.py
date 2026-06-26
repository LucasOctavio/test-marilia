from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioLogin(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    nivel: int
    acerto_total: int
    erro_total: int

    class Config:
        from_attributes = True

class MensagemResponse(BaseModel):
    mensagem: str


class UsuarioMensagemResponse(BaseModel):
    mensagem: str
    usuario: UsuarioResponse


class UsuarioUpdateProgresso(BaseModel):
    acerto_total: int
    erro_total: int