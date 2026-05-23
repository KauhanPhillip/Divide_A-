from fastapi import FastAPI
from app.routes import usuarios, grupos, membros, despesas
from app.database import engine, Base
from app.routes import auth

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Divide Aí API",
    description="Backend Inteligente para Divisão de Gastos em Grupo",
    version="1.0.0"
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