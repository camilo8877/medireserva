from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.seguridad import verificar_token
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verificar_token(token, tipo_esperado="access")
    if payload is None:
        raise credenciales_invalidas

    try:
        usuario_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise credenciales_invalidas

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise credenciales_invalidas

    return usuario


def requerir_medico(
    usuario: Usuario = Depends(obtener_usuario_actual)
) -> Usuario:
    if usuario.rol != "medico":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de médico"
        )
    return usuario


def requerir_admin(
    usuario: Usuario = Depends(obtener_usuario_actual)
) -> Usuario:
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de administrador"
        )
    return usuario