from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PatientBase(BaseModel):
    name: str
    gender: Optional[str]
    age: Optional[int]
    phone: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_name: str
    appointment_datetime: datetime

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    status: str

    class Config:
        orm_mode = True


class ConsultationBase(BaseModel):
    appointment_id: int
    patient_id: int
    vitals_1: Optional[str]
    vitals_2: Optional[str]
    notes: Optional[str]

class ConsultationCreate(ConsultationBase):
    pass

class Consultation(ConsultationBase):
    id: int
    status: str

    class Config:
        orm_mode = True