# app/services/medico_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.medico import Medico
from app.models.usuario import Usuario


def crear_perfil_medico(db: Session, usuario_id: int, especialidad: str) -> Medico:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existente = db.query(Medico).filter(Medico.usuario_id == usuario_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Este usuario ya tiene perfil de médico")

    usuario.rol = "medico"

    nuevo_perfil = Medico(usuario_id=usuario_id, especialidad=especialidad)
    db.add(nuevo_perfil)
    db.commit()
    db.refresh(nuevo_perfil)
    return nuevo_perfil


def listar_medicos(db: Session):
    return db.query(Medico).all()