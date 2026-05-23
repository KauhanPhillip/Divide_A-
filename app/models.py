from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # Importe o UUID
import uuid
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    # Use as_uuid=True para o SQLAlchemy lidar com objetos UUID do Python
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)

class Grupo(Base):
    __tablename__ = "grupos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    criador_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    criador = relationship("Usuario")

class GrupoMembro(Base):
    __tablename__ = "grupo_membros"
    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)

class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos.id"), nullable=False)
    pagador_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    valor = Column(Float, nullable=False) # Lembre-se de importar Float
    descricao = Column(String, nullable=False)
    categoria = Column(String, nullable=True)