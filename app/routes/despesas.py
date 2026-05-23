from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from uuid import UUID
from fastapi import HTTPException
from app.deps import obter_usuario_atual

router = APIRouter(prefix="/despesas", tags=["Despesas"])

# --- CRIAR DESPESA ---
@router.post("/", response_model=schemas.DespesaResponse)
def criar_despesa(despesa: schemas.DespesaCreate, db: Session = Depends(get_db)):
    nova_despesa = models.Despesa(**despesa.model_dump())
    db.add(nova_despesa)
    db.commit()
    db.refresh(nova_despesa)
    return nova_despesa

# --- LISTAR DESPESAS POR GRUPO ---
@router.get("/{grupo_id}", response_model=List[schemas.DespesaResponse])
def listar_despesas_por_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    despesas = db.query(models.Despesa).filter(models.Despesa.grupo_id == grupo_id).all()
    return despesas

# --- DELETAR DESPESA ---
@router.delete("/{despesa_id}")
def deletar_despesa(despesa_id: UUID, db: Session = Depends(get_db)):
    despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    db.delete(despesa)
    db.commit()
    return {"message": "Despesa deletada com sucesso"}

# --- EDITA DESPESA ---
@router.put("/{despesa_id}")
def editar_despesa(despesa_id: UUID, despesa_data: schemas.DespesaCreate, db: Session = Depends(get_db)):
    despesa = db.query(models.Despesa).filter(models.Despesa.id == despesa_id).first()
    
    if not despesa:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    # Atualiza os campos
    despesa.valor = despesa_data.valor
    despesa.descricao = despesa_data.descricao
    despesa.categoria = despesa_data.categoria
    despesa.pagador_id = despesa_data.pagador_id
    despesa.grupo_id = despesa_data.grupo_id
    
    db.commit()
    db.refresh(despesa)
    return despesa

# --- SOMA DESPESAS ---
@router.get("/{grupo_id}/saldo")
def calcular_saldo_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    # Fazemos uma junção (join) com a tabela de usuários para pegar o nome
    resultados = db.query(
        models.Usuario.nome, 
        func.sum(models.Despesa.valor).label("total_pago")
    ).join(models.Despesa, models.Usuario.id == models.Despesa.pagador_id)\
     .filter(models.Despesa.grupo_id == grupo_id)\
     .group_by(models.Usuario.nome).all()
    
    return [{"usuario": r[0], "total_pago": float(r[1])} for r in resultados]

# ---DIVISÃO ---
@router.get("/{grupo_id}/divisao")
def calcular_divisao(grupo_id: UUID, db: Session = Depends(get_db)):
    # 1. Total de membros cadastrados no grupo
    total_membros = db.query(models.Membro).filter(models.Membro.grupo_id == grupo_id).count()
    
    if total_membros == 0:
        return {"mensagem": "O grupo não possui membros cadastrados."}

    # 2. Total pago por cada um
    pagamentos = db.query(
        models.Usuario.nome, 
        func.sum(models.Despesa.valor).label("total_pago")
    ).join(models.Despesa, models.Usuario.id == models.Despesa.pagador_id)\
     .filter(models.Despesa.grupo_id == grupo_id)\
     .group_by(models.Usuario.nome).all()

    total_grupo = sum(p[1] for p in pagamentos)
    media = total_grupo / total_membros
    
    # 3. Criar a lista de saldo (quem pagou - media)
    # Nota: para os usuários que não pagaram nada, precisaremos incluí-los aqui no futuro
    resultado = [
        {"usuario": p[0], "saldo": round(p[1] - media, 2)} 
        for p in pagamentos
    ]
    
    return {
        "total_grupo": total_grupo, 
        "num_membros": total_membros,
        "media_por_pessoa": round(media, 2), 
        "detalhes": resultado
    }

# --- CRIAR DESPESA (PROTEGIDA) ---
@router.post("/", response_model=schemas.DespesaResponse)
def criar_despesa(
    despesa: schemas.DespesaCreate, 
    db: Session = Depends(get_db),
    usuario_email: str = Depends(obter_usuario_atual) # Segurança aplicada!
):
    nova_despesa = models.Despesa(**despesa.model_dump())
    db.add(nova_despesa)
    db.commit()
    db.refresh(nova_despesa)
    return nova_despesa