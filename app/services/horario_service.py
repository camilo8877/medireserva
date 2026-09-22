from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.horario import Horario
from app.models.medico import Medico


def obtener_perfil_medico(db: Session, usuario_id: int) -> Medico:
    perfil = db.query(Medico).filter(Medico.usuario_id == usuario_id).first()
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuario no tiene un perfil de médico asociado"
        )
    return perfil


def crear_horario(
    db: Session,
    dia_semana: str,
    hora_inicio: str,
    hora_fin: str,
    usuario_id: int
) -> Horario:
    perfil = obtener_perfil_medico(db, usuario_id)

    nuevo_horario = Horario(
        medico_id=perfil.id,
        dia_semana=dia_semana,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin
    )
    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)
    return nuevo_horario


def listar_horarios(db: Session):
    return db.query(Horario).all()


def obtener_horario(db: Session, horario_id: int) -> Horario:
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


def _verificar_dueno(horario: Horario, usuario_id: int, rol: str):
    if horario.medico.usuario_id != usuario_id and rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este horario no te pertenece"
        )


def actualizar_horario(
    db: Session,
    horario_id: int,
    dia_semana: str,
    hora_inicio: str,
    hora_fin: str,
    usuario_id: int,
    rol: str
) -> Horario:
    horario = obtener_horario(db, horario_id)
    _verificar_dueno(horario, usuario_id, rol)

    horario.dia_semana = dia_semana
    horario.hora_inicio = hora_inicio
    horario.hora_fin = hora_fin
    db.commit()
    db.refresh(horario)
    return horario


def eliminar_horario(db: Session, horario_id: int, usuario_id: int, rol: str) -> None:
    horario = obtener_horario(db, horario_id)
    _verificar_dueno(horario, usuario_id, rol)

    db.delete(horario)
    db.commit()