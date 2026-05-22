from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario  # <-- Certifique-se de que o import do seu modelo está correto!
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# 1. Esquema do Pydantic para o Cadastro (Você provavelmente já tem algo assim)
class UsuarioCadastroSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

# 2. Esquema do Pydantic para o Login (Obrigatório estar ANTES da função de login)
class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

# 3. Rota de Cadastro existente
@router.post("/")
def cadastrar_usuario(usuario: UsuarioCadastroSchema, db: Session = Depends(get_db)):
    # Verifica se o e-mail já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    # Cria a nova instância incluindo a senha
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha  # <-- Garanta que esta linha existe!
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {"mensagem": "Usuário cadastrado com sucesso!"}

# 4. Sua Rota de Login Nova
@router.post("/login")
def login(dados_login: LoginSchema, db: Session = Depends(get_db)):
    # 1. Busca o usuário pelo e-mail
    usuario = db.query(Usuario).filter(Usuario.email == dados_login.email).first()
    
    # 2. Se o usuário não existir, retorna erro 401
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    # 3. Verifica a senha
    if usuario.senha != dados_login.senha:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    # 4. Login bem-sucedido
    return {
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    }