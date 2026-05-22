import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega a URL do ambiente de forma segura
raw_url = os.getenv("DATABASE_URL", "")

def obter_url_limpa(url: str) -> str:
    """Limpa e corrige a string de conexão para evitar falhas do .env"""
    if not url:
        return ""
        
    # Remove o prefixo se ele veio duplicado (ex: DATABASE_URL=postgresql://...)
    if url.startswith("DATABASE_URL="):
        url = url.replace("DATABASE_URL=", "")
        
    # Garante que usamos a porta 5432 de conexão direta em vez do pooler 6543
    if ":6543/" in url:
        url = url.replace(":6543/", ":5432/")
        
    return url.strip()

DATABASE_URL = obter_url_limpa(raw_url)

if not DATABASE_URL:
    raise ValueError("ERRO: A variável DATABASE_URL não foi encontrada no seu arquivo .env!")

# O print agora só mostra o começo do link por segurança
print(f"--> [Seguro] Conectando em: {DATABASE_URL[:25]}...")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()