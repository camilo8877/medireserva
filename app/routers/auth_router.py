from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioRespuesta
from app.schemas.token import Token, TokenRefresh, TokenAccesoNuevo
from app.services.usuario_service import registrar_usuario
from app.models.usuario import Usuario
from app.auth.seguridad import (
    verificar_password,
    crear_access_token,
    crear_refresh_token,
    verificar_token,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registro", response_model=UsuarioRespuesta)
def registro(datos: UsuarioCreate, db: Session = Depends(get_db)):
    return registrar_usuario(db, datos)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    datos_token = {"sub": str(usuario.id)}
    access_token = crear_access_token(datos_token)
    refresh_token = crear_refresh_token(datos_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenAccesoNuevo)
def refrescar(datos: TokenRefresh, db: Session = Depends(get_db)):
    payload = verificar_token(datos.refresh_token, tipo_esperado="refresh")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        usuario_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    nuevo_access = crear_access_token({"sub": str(usuario.id)})
    return {"access_token": nuevo_access, "token_type": "bearer"}