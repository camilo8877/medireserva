from pydantic import BaseModel

class HorarioCreate(BaseModel):
    dia_semana: str
    hora_inicio: str
    hora_fin: str

class HorarioRespuesta(BaseModel):
    id: int
    medico_id: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str
    estado: str

    class Config:
        from_attributes = True
