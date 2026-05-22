import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # ADICIONE ESTA LINHA EXATAMENTE AQUI:
    senha = Column(String, nullable=False)
    
    # Se você ainda tiver o firebase_uid aí, pode deixar ele aqui embaixo:
    firebase_uid = Column(String, nullable=True)