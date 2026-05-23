from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import verificar_senha, criar_token

router = APIRouter(tags=["Autenticação"])

@router.post("/login")
def login(usuario_login: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario_login.email).first()
    
    if not usuario or not verificar_senha(usuario_login.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
    
    token = criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}