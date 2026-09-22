from fastapi import FastAPI
from app.database import Base, engine

from app.models import usuario, medico, horario, cita

from app.routers import auth_router, medico_router, horario_router, cita_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediReserva API", description="Backend del sistema de reservas de citas médicas")

app.include_router(auth_router.router)
app.include_router(medico_router.router)
app.include_router(horario_router.router)
app.include_router(cita_router.router)


@app.get("/")
def raiz():
    return {"mensaje": "MediReserva API funcionando"}