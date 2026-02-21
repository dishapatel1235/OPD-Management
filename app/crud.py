
from sqlalchemy.orm import Session
from datetime import datetime, date
from . import models

def create_patient(db: Session, patient_data):
    patient = models.Patient(**patient_data)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patients(db: Session, search: str = None):
    query = db.query(models.Patient)

    if search:
        query = query.filter(
            (models.Patient.name.contains(search)) |
            (models.Patient.phone.contains(search))
        )

    return query.all()



def create_appointment(db: Session, data):
    patient = db.query(models.Patient).filter_by(id=data["patient_id"]).first()


    if patient.status == models.PatientStatus.Inactive:
        raise ValueError("Cannot create appointment for inactive patient")


    if data["appointment_datetime"] < datetime.utcnow():
        raise ValueError("Appointment cannot be in the past")

    appt = models.Appointment(**data)
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


def get_today_appointments(db: Session):
    today = date.today()
    return db.query(models.Appointment).filter(
        models.Appointment.appointment_datetime >= today
    ).all()



def create_consultation(db: Session, data):
    appt = db.query(models.Appointment).filter_by(id=data["appointment_id"]).first()


    if appt.status != models.AppointmentStatus.Scheduled:
        raise ValueError("Consultation allowed only for scheduled appointments")

   
    existing = db.query(models.Consultation).filter_by(
        appointment_id=data["appointment_id"]
    ).first()

    if existing:
        raise ValueError("Consultation already exists for this appointment")

    consultation = models.Consultation(**data)
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    return consultation


def complete_consultation(db: Session, consult_id: int):
    consult = db.query(models.Consultation).get(consult_id)
    consult.status = models.ConsultationStatus.Completed
    consult.appointment.status = models.AppointmentStatus.Completed

    db.commit()
    return consult