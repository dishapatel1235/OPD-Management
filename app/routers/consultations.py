from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, models

router = APIRouter()

@router.get("/consultations/new/{appointment_id}", response_class=HTMLResponse)
def new_consultation(request: Request, appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).get(appointment_id)
    return request.app.state.templates.TemplateResponse(
        "consultation_form.html",
        {
            "request": request,
            "appointment_id": appointment_id,
            "patient_id": appointment.patient_id
        }
    )

@router.post("/consultations/create")
def create_consultation(
    appointment_id: int = Form(...),
    patient_id: int = Form(...),
    vitals_1: str = Form(None),
    vitals_2: str = Form(None),
    notes: str = Form(None),
    db: Session = Depends(get_db),
):
    crud.create_consultation(db, {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "vitals_1": vitals_1,
        "vitals_2": vitals_2,
        "notes": notes,
    })
    return RedirectResponse("/appointments/today", status_code=303)

@router.post("/consultations/complete/{id}")
def complete_consultation(id: int, db: Session = Depends(get_db)):
    crud.complete_consultation(db, id)
    return RedirectResponse("/appointments/today", status_code=303)