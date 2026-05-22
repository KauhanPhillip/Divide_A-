from fastapi import FastAPI
from app.routes import usuarios  # <-- Certifique-se de que essa linha existe!

app = FastAPI(
    title="Divide Aí API",
    description="Backend Inteligente para Divisão de Gastos em Grupo",
    version="1.0.0"
)

# Puxa as rotas de usuários para dentro do Swagger
app.include_router(usuarios.router)

@app.get("/")
def home():
    return {"status": "API do Divide Aí rodando perfeitamente!"}