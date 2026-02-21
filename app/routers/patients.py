from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud

router = APIRouter()

@router.get("/patients", response_class=HTMLResponse)
def list_patients(request: Request, search: str = "", db: Session = Depends(get_db)):
    patients = crud.get_patients(db, search)
    return request.app.state.templates.TemplateResponse(
        "patients.html",
        {"request": request, "patients": patients}
    )

@router.get("/patients/new", response_class=HTMLResponse)
def new_patient_form(request: Request):
    return request.app.state.templates.TemplateResponse(
        "patient_form.html", {"request": request}
    )

@router.post("/patients/create")
def create_patient(
    name: str = Form(...),
    gender: str = Form(...),
    age: int = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db),
):
    crud.create_patient(db, {"name": name, "gender": gender, "age": age, "phone": phone})
    return RedirectResponse("/patients", status_code=303)