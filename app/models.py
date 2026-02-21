from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class PatientStatus(str, enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class AppointmentStatus(str, enum.Enum):
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"

class ConsultationStatus(str, enum.Enum):
    Draft = "Draft"
    Completed = "Completed"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10))
    age = Column(Integer)
    phone = Column(String(15), unique=True)
    status = Column(Enum(PatientStatus), default=PatientStatus.Active)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="patient")
    consultations = relationship("Consultation", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_name = Column(String(100))
    appointment_datetime = Column(DateTime)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.Scheduled)

    patient = relationship("Patient", back_populates="appointments")
    consultation = relationship("Consultation", back_populates="appointment", uselist=False)


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    vitals_1 = Column(String(100))
    vitals_2 = Column(String(100))
    notes = Column(String(500))
    status = Column(Enum(ConsultationStatus), default=ConsultationStatus.Draft)

    appointment = relationship("Appointment", back_populates="consultation")
    patient = relationship("Patient", back_populates="consultations")