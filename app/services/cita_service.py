from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cita import Cita
from app.models.medico import Medico


def _verificar_medico_existe(db: Session, medico_id: int) -> Medico:
    medico = db.query(Medico).filter(Medico.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    return medico


def agendar_cita(db: Session, paciente_id: int, medico_id: int, fecha_hora) -> Cita:
    _verificar_medico_existe(db, medico_id)

    nueva_cita = Cita(
        paciente_id=paciente_id,
        medico_id=medico_id,
        fecha_hora=fecha_hora,
        estado="pendiente"
    )
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita


def listar_mis_citas(db: Session, paciente_id: int):
    return db.query(Cita).filter(Cita.paciente_id == paciente_id).all()


def obtener_cita(db: Session, cita_id: int) -> Cita:
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita


def cancelar_cita(db: Session, cita_id: int, paciente_id: int, rol: str) -> Cita:
    cita = obtener_cita(db, cita_id)

    if cita.paciente_id != paciente_id and rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta cita no te pertenece"
        )

    cita.estado = "cancelada"
    db.commit()
    db.refresh(cita)
    return cita