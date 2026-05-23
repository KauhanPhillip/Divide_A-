from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import usuarios, grupos, membros, despesas, auth
from app.database import engine, Base
from app.routes import auth

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Divide Aí API",
    description="Backend Inteligente para Divisão de Gastos em Grupo",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite todos os domínios (ideal para testes)
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Puxa as rotas para dentro do Swagger
app.include_router(usuarios.router)
app.include_router(grupos.router)
app.include_router(membros.router)
app.include_router(despesas.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"status": "API do Divide Aí rodando perfeitamente!"}