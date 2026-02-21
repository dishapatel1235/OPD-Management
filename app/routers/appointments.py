from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, models

router = APIRouter()

@router.get("/appointments/today", response_class=HTMLResponse)
def today_appointments(request: Request, db: Session = Depends(get_db)):
    appts = crud.get_today_appointments(db)
    return request.app.state.templates.TemplateResponse(
        "appointments.html",
        {"request": request, "appointments": appts}
    )

@router.get("/appointments/new", response_class=HTMLResponse)
def new_appointment_form(request: Request, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).filter_by(status="Active").all()
    return request.app.state.templates.TemplateResponse(
        "appointment_form.html",
        {"request": request, "patients": patients}
    )

from datetime import datetime

@router.post("/appointments/create")
def create_appointment(
    patient_id: int = Form(...),
    doctor_name: str = Form(...),
    appointment_datetime: str = Form(...),
    db: Session = Depends(get_db),
):

    appointment_dt = datetime.fromisoformat(appointment_datetime)

    crud.create_appointment(db, {
        "patient_id": patient_id,
        "doctor_name": doctor_name,
        "appointment_datetime": appointment_dt,
    })
    return RedirectResponse("/appointments/today", status_code=303)