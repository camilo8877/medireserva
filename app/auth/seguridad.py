from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano[:72], password_hash)

def crear_access_token(datos: dict) -> str:
    datos_a_codificar = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    datos_a_codificar.update({"exp": expira, "tipo": "access"})
    return jwt.encode(datos_a_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def crear_refresh_token(datos: dict) -> str:
    datos_a_codificar = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    datos_a_codificar.update({"exp": expira, "tipo": "refresh"})
    return jwt.encode(datos_a_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verificar_token(token: str, tipo_esperado: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("tipo") != tipo_esperado:
            return None
        return payload
    except JWTError:
        return None
