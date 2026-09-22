from datetime import datetime
from pydantic import BaseModel

class CitaCreate(BaseModel):
    horario_id: int
    fecha_hora: datetime

class CitaRespuesta(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    horario_id: int
    fecha_hora: datetime
    estado: str

    class Config:
        from_attributes = True
