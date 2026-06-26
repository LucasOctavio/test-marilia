from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

# --- PERGUNTA ---
class PerguntaBase(BaseModel):
    pergunta: str
    alternativas: Optional[Dict[str, Any]] = None  
    resposta: Optional[str] = Field(None, max_length=1)
    feedback: Optional[str] = None

class PerguntaCreate(PerguntaBase):
    categoria: Optional[int] = None

class PerguntaResponse(PerguntaBase):
    id: int
    categoria: Optional[int] = None

    class Config:
        from_attributes = True


class PerguntaMensagemResponse(BaseModel):
    mensagem: str
    pergunta: PerguntaResponse

