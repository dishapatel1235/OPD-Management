from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from app.database import engine
from app import models
from app.routers import patients, appointments, consultations

app = FastAPI()

app.state.templates = Jinja2Templates(directory="app/templates")

models.Base.metadata.create_all(bind=engine)

app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(consultations.router)