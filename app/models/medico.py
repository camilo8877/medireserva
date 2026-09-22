from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    # El perfil de médico extiende a un Usuario (con rol "medico").
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    especialidad = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="perfil_medico")
    horarios = relationship("Horario", back_populates="medico")
    citas = relationship("Cita", back_populates="medico")
