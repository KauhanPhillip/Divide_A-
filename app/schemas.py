from pydantic import BaseModel, EmailStr
from uuid import UUID # Importação necessária
from typing import Optional
from datetime import datetime

# --- USUÁRIOS ---
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    firebase_uid: Optional[str] = None
    foto_url: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioResponse(BaseModel):
    id: UUID  # Alterado de int para UUID
    nome: str
    email: str
    foto_url: Optional[str]

    class Config:
        from_attributes = True

# --- GRUPOS ---
class GrupoBase(BaseModel):
    nome: str

class GrupoCreate(GrupoBase):
    criador_id: UUID # Alterado de int para UUID

class GrupoResponse(GrupoBase):
    id: UUID  # Alterado de int para UUID
    criador_id: UUID # Alterado de int para UUID
    
    class Config:
        from_attributes = True

# --- MEMBROS ---

class MembroCreate(BaseModel):
    grupo_id: UUID
    usuario_id: UUID

class MembroResponse(MembroCreate):
    id: UUID  # Alterado de int para UUID para manter consistência
    
    class Config:
        from_attributes = True

# --- DESPESAS ---
class DespesaCreate(BaseModel):
    grupo_id: UUID
    pagador_id: UUID
    valor: float
    descricao: str
    categoria: str

class DespesaResponse(DespesaCreate):
    id: UUID
    
    class Config:
        from_attributes = True