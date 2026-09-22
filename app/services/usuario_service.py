from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.auth.seguridad import hashear_password

def registrar_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    existente = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # El rol SIEMPRE se fija en el servidor como "paciente".
    # Si se permitiera elegir el rol desde el registro, cualquiera
    # podría enviar {"rol": "admin"} y tomar control del sistema.
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        password_hash=hashear_password(datos.password),
        rol="paciente"
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario
