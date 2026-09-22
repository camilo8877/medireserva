from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    # Todo el que se registra por este endpoint queda como "paciente".
    
    rol = Column(String, nullable=False, default="paciente")

    # Un usuario con rol "medico" tiene un perfil de Medico asociado (1 a 1).
    perfil_medico = relationship("Medico", back_populates="usuario", uselist=False)
    # Un usuario con rol "paciente" puede tener muchas citas.
    citas_como_paciente = relationship("Cita", back_populates="paciente")
