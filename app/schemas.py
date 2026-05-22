from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

# O que o Flutter precisa enviar para cadastrar um usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    firebase_uid: Optional[str] = None
    foto_url: Optional[str] = None

# Como a API vai devolver o usuário para o Flutter
class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    email: str
    foto_url: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True