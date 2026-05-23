from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/grupos", tags=["Grupos"])

# Corrigido para schemas.GrupoResponse
@router.post("/", response_model=schemas.GrupoResponse)
def criar_grupo(grupo: schemas.GrupoCreate, db: Session = Depends(get_db)):
    novo_grupo = models.Grupo(nome=grupo.nome, criador_id=grupo.criador_id)
    db.add(novo_grupo)
    db.commit()
    db.refresh(novo_grupo)
    return novo_grupo