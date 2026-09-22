from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    # Estos dos campos son la base de la autorización de la Parte 2:
    # cada cita "sabe" de qué paciente y de qué médico es.
    paciente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    horario_id = Column(Integer, ForeignKey("horarios.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String, nullable=False, default="pendiente")

    paciente = relationship("Usuario", back_populates="citas_como_paciente")
    medico = relationship("Medico", back_populates="citas")
