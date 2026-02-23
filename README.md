🧭 Application Flow
The OPD Management System is a server-rendered web application built using FastAPI, SQLAlchemy, MySQL, and Jinja2 templates. It manages patients, appointments, and consultations through a status-driven workflow.

🛠️ Tech Stack
Backend: FastAPI, SQLAlchemy
Database: MySQL
Templates: Jinja2 + Bootstrap
Server: Uvicorn / Gunicorn
Flow Overview :

1. Patient Registration :
User creates a new patient via the Patient form.
Patient is stored with default status Active.

2. Appointment Booking :
User selects an Active patient.
Books an appointment with doctor name and date/time.
Appointment is created with default status Scheduled.

3. Consultation Workflow :
Consultation can be started only for Scheduled appointments.
Consultation begins in Draft status.
When marked Completed, the related appointment automatically becomes Completed.

Viewing Data :
Users can:
Search patients
View today's appointments
Start consultations
View consultation status

This ensures the workflow is controlled by the backend and follows business rules.

🗄️ Table Relationships
The application uses a relational database with the following relationships:

1. Patients Table
Primary entity storing patient information.
One patient can have multiple appointments and consultations.

2. Appointments Table
Linked to patients using patient_id.
One appointment belongs to one patient.
One appointment can have only one consultation.

3. Consultations Table
Linked to both appointment and patient.
Ensures consultation history per patient.

Relationship Diagram (Logical)
Patient (1) ────< Appointments (Many)
Patient (1) ────< Consultations (Many)
Appointment (1) ────< Consultation (1)


🔄 Status & Workflow Rules
The system enforces strict backend rules to maintain data integrity.

Patient Rules : 
Default status: Active
Only Active patients can book appointments.

Appointment Rules :
Default status: Scheduled
Cannot be created:
For inactive patients
In the past
Automatically changes to Completed when consultation is completed.

Consultation Rules :
Can only be created if appointment status is Scheduled.
Only one consultation per appointment is allowed.
Default status: Draft
When marked Completed:
Consultation → Completed
Appointment → Completed
Validation Enforcement

All rules are enforced on the server side using business logic in crud.py.
Invalid state transitions are blocked.

▶️ How to Run Locally?

1️⃣ Clone Repository
git clone https://github.com/yourusername/opd-management-system.git
cd opd-management-system

2️⃣ Create Virtual Environment
python -m venv .venv
Activate:
Windows : .venv\Scripts\activate
Mac/Linux : source .venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Database
Update app/database.py:
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://USER:PASSWORD@localhost:3306/opd_db"
Create database in MySQL:
CREATE DATABASE opd_db;

5️⃣ Run Application (Development)
uvicorn main:app --reload
Open in browser:
👉 http://127.0.0.1:8000/patients

6️⃣ Run with Gunicorn (Production)
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

🧪 Test URLs
/patients → List & search patients
/patients/new → Add patient
/appointments/new → Book appointment
/appointments/today → Today’s appointments
/consultations/new/{appointment_id} → Start consultation

