from pydantic import BaseModel
from typing import Optional

# --- USUÁRIO ---
class UsuarioBase(BaseModel):
    nome: str

class UsuarioAuthSchema(UsuarioBase):
    senha: str

class UsuarioResponseSchema(UsuarioBase):
    id: int
    nivel: Optional[int] = None
    acerto_total: Optional[int] = None
    erro_total: Optional[int] = None

    class Config:
        from_attributes = True