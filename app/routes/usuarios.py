from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario
from pydantic import BaseModel, EmailStr
from app.deps import obter_usuario_atual
from app.security import hash_senha, verificar_senha 

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# Esquemas
class UsuarioCadastroSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

# Rota de Cadastro
@router.post("/")
def cadastrar_usuario(usuario: UsuarioCadastroSchema, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    # Converte a senha para hash
    senha_hash = hash_senha(usuario.senha)
    
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {"mensagem": "Usuário cadastrado com sucesso!"}

# Rota de Login (CORRIGIDA)
@router.post("/login")
def login(dados_login: LoginSchema, db: Session = Depends(get_db)):
    # 1. Busca o usuário pelo e-mail
    usuario = db.query(Usuario).filter(Usuario.email == dados_login.email).first()
    
    # 2. Verifica se o usuário existe E se a senha é válida (usando o hash)
    # A função verificar_senha faz a comparação segura entre o texto puro e o hash
    if not usuario or not verificar_senha(dados_login.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    # 3. Login bem-sucedido
    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }