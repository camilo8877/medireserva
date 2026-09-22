# app/routers/medico_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.medico import MedicoCreate, MedicoRespuesta
from app.services.medico_service import crear_perfil_medico, listar_medicos
from app.auth.dependencias import requerir_admin
from app.models.usuario import Usuario

router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.get("/", response_model=list[MedicoRespuesta])
def get_medicos(db: Session = Depends(get_db)):
    return listar_medicos(db)


@router.post("/", response_model=MedicoRespuesta)
def post_medico(
    datos: MedicoCreate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(requerir_admin)
):
    return crear_perfil_medico(db, datos.usuario_id, datos.especialidad)