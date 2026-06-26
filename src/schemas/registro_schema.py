from pydantic import BaseModel
from typing import Optional

# --- REGISTRO ---
class RegistroBase(BaseModel):
    acerto_categoria: Optional[int] = None

class RegistroCreate(RegistroBase):
    categoria_id: Optional[int] = None
    user_id: Optional[int] = None

class RegistroResponse(RegistroBase):
    id: int
    categoria_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class RegistroMensagemResponse(BaseModel):
    mensagem: str
    registro: RegistroResponse
