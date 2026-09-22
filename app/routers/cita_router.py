from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cita import CitaCreate, CitaRespuesta
from app.services.cita_service import (
    agendar_cita,
    listar_mis_citas,
    cancelar_cita,
)
from app.auth.dependencias import obtener_usuario_actual
from app.models.usuario import Usuario

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.post("/", response_model=CitaRespuesta)
def post_cita(
    datos: CitaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return agendar_cita(db, usuario.id, datos.medico_id, datos.fecha_hora)


@router.get("/mis-citas", response_model=list[CitaRespuesta])
def get_mis_citas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return listar_mis_citas(db, usuario.id)


@router.delete("/{cita_id}", response_model=CitaRespuesta)
def delete_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    return cancelar_cita(db, cita_id, usuario.id, usuario.rol)