from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.deps import obter_usuario_atual

router = APIRouter(prefix="/membros", tags=["Membros"])

@router.post("/", response_model=schemas.MembroResponse)
def adicionar_membro(membro: schemas.MembroCreate, db: Session = Depends(get_db)):
    novo_membro = models.GrupoMembro(grupo_id=membro.grupo_id, usuario_id=membro.usuario_id)
    db.add(novo_membro)
    db.commit()
    db.refresh(novo_membro)
    return novo_membro