from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.horario import HorarioCreate, HorarioRespuesta
from app.services.horario_service import (
    crear_horario,
    listar_horarios,
    actualizar_horario,
    eliminar_horario,
)
from app.auth.dependencias import requerir_medico
from app.models.usuario import Usuario

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/", response_model=list[HorarioRespuesta])
def get_horarios(db: Session = Depends(get_db)):
    return listar_horarios(db)


@router.post("/", response_model=HorarioRespuesta)
def post_horario(
    datos: HorarioCreate,
    db: Session = Depends(get_db),
    medico: Usuario = Depends(requerir_medico)
):
    return crear_horario(
        db,
        datos.dia_semana,
        datos.hora_inicio,
        datos.hora_fin,
        medico.id
    )


@router.put("/{horario_id}", response_model=HorarioRespuesta)
def put_horario(
    horario_id: int,
    datos: HorarioCreate,
    db: Session = Depends(get_db),
    medico: Usuario = Depends(requerir_medico)
):
    return actualizar_horario(
        db,
        horario_id,
        datos.dia_semana,
        datos.hora_inicio,
        datos.hora_fin,
        medico.id,
        medico.rol
    )


@router.delete("/{horario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_horario(
    horario_id: int,
    db: Session = Depends(get_db),
    medico: Usuario = Depends(requerir_medico)
):
    eliminar_horario(db, horario_id, medico.id, medico.rol)