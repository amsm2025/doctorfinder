from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="HMO Doctor Finder API",
    version="1.0.0",
    description="Demo API for searching HMO-accredited doctors and creating appointment requests."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCTORS = [
    {"id": 1, "name": "Dr. Sofia Reyes", "gender": "F", "specialty": "Internal Medicine", "location": "Pasig City", "clinic": "MetroCare Medical Center", "hmos": ["Maxicare", "Intellicare", "MediCard"], "rating": 4.9, "experience_years": 12, "teleconsult": True, "weekend": True, "availability": "today", "next_available": "Today, 2:30 PM", "verified": True, "patient_types": ["adult", "senior"]},
    {"id": 2, "name": "Dr. Miguel Santos", "gender": "M", "specialty": "Cardiology", "location": "Makati City", "clinic": "Central Heart Institute", "hmos": ["Maxicare", "PhilCare", "Etiqa"], "rating": 4.8, "experience_years": 17, "teleconsult": True, "weekend": False, "availability": "tomorrow", "next_available": "Tomorrow, 10:00 AM", "verified": True, "patient_types": ["adult", "senior"]},
    {"id": 3, "name": "Dr. Angela Cruz", "gender": "F", "specialty": "Pediatrics", "location": "Quezon City", "clinic": "Northview Children's Clinic", "hmos": ["Intellicare", "MediCard", "ValuCare"], "rating": 4.9, "experience_years": 10, "teleconsult": True, "weekend": True, "availability": "today", "next_available": "Today, 4:00 PM", "verified": True, "patient_types": ["child"]},
    {"id": 4, "name": "Dr. Carlo Mendoza", "gender": "M", "specialty": "Orthopedics", "location": "Taguig City", "clinic": "BGC Specialty Center", "hmos": ["Maxicare", "Intellicare", "Etiqa"], "rating": 4.7, "experience_years": 14, "teleconsult": False, "weekend": True, "availability": "week", "next_available": "Friday, 9:30 AM", "verified": True, "patient_types": ["adult", "senior"]},
    {"id": 5, "name": "Dr. Patricia Lim", "gender": "F", "specialty": "Dermatology", "location": "Mandaluyong City", "clinic": "Skin & Wellness Hub", "hmos": ["MediCard", "PhilCare", "ValuCare"], "rating": 4.8, "experience_years": 9, "teleconsult": True, "weekend": True, "availability": "tomorrow", "next_available": "Tomorrow, 1:00 PM", "verified": True, "patient_types": ["adult", "child"]},
    {"id": 6, "name": "Dr. Ramon Villanueva", "gender": "M", "specialty": "ENT", "location": "Manila", "clinic": "Manila Specialty Hospital", "hmos": ["Maxicare", "Intellicare", "PhilCare"], "rating": 4.6, "experience_years": 18, "teleconsult": False, "weekend": False, "availability": "week", "next_available": "Thursday, 3:00 PM", "verified": True, "patient_types": ["adult", "child", "senior"]},
    {"id": 7, "name": "Dr. Camille Navarro", "gender": "F", "specialty": "OB-GYN", "location": "Pasig City", "clinic": "Women's Health Pavilion", "hmos": ["Maxicare", "MediCard", "Etiqa"], "rating": 5.0, "experience_years": 13, "teleconsult": True, "weekend": False, "availability": "today", "next_available": "Today, 5:30 PM", "verified": True, "patient_types": ["adult"]},
    {"id": 8, "name": "Dr. Leo Garcia", "gender": "M", "specialty": "Family Medicine", "location": "Quezon City", "clinic": "Family First Clinic", "hmos": ["Maxicare", "Intellicare", "MediCard", "PhilCare", "ValuCare"], "rating": 4.8, "experience_years": 11, "teleconsult": True, "weekend": True, "availability": "today", "next_available": "Today, 6:00 PM", "verified": True, "patient_types": ["adult", "child", "senior"]},
    {"id": 9, "name": "Dr. Nina Flores", "gender": "F", "specialty": "Psychiatry", "location": "Makati City", "clinic": "Mindwell Center", "hmos": ["Intellicare", "MediCard", "Etiqa"], "rating": 4.9, "experience_years": 8, "teleconsult": True, "weekend": True, "availability": "tomorrow", "next_available": "Tomorrow, 11:30 AM", "verified": True, "patient_types": ["adult", "senior"]},
    {"id": 10, "name": "Dr. Jose Aquino", "gender": "M", "specialty": "Internal Medicine", "location": "Taguig City", "clinic": "South Metro Clinic", "hmos": ["PhilCare", "Etiqa", "ValuCare"], "rating": 4.5, "experience_years": 7, "teleconsult": True, "weekend": False, "availability": "week", "next_available": "Friday, 2:00 PM", "verified": False, "patient_types": ["adult", "senior"]},
    {"id": 11, "name": "Dr. Bea Tan", "gender": "F", "specialty": "Cardiology", "location": "Pasig City", "clinic": "East Metro Heart Center", "hmos": ["Maxicare", "Intellicare", "MediCard"], "rating": 4.9, "experience_years": 15, "teleconsult": True, "weekend": True, "availability": "tomorrow", "next_available": "Tomorrow, 8:30 AM", "verified": True, "patient_types": ["adult", "senior"]},
    {"id": 12, "name": "Dr. Kevin Yu", "gender": "M", "specialty": "Family Medicine", "location": "Mandaluyong City", "clinic": "CityCare Primary Clinic", "hmos": ["Maxicare", "PhilCare", "ValuCare"], "rating": 4.7, "experience_years": 6, "teleconsult": True, "weekend": True, "availability": "today", "next_available": "Today, 7:00 PM", "verified": True, "patient_types": ["adult", "child", "senior"]}
]

APPOINTMENTS = []

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_name: str = Field(min_length=2, max_length=120)
    hmo_provider: str
    membership_no: Optional[str] = None
    preferred_date: str
    consultation_type: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "hmo-doctor-finder-api"}

@app.get("/meta")
def meta():
    return {
        "hmos": sorted({h for d in DOCTORS for h in d["hmos"]}),
        "specialties": sorted({d["specialty"] for d in DOCTORS}),
        "locations": sorted({d["location"] for d in DOCTORS})
    }

@app.get("/doctors")
def list_doctors(
    hmo: Optional[str] = None,
    specialty: Optional[str] = None,
    location: Optional[str] = None,
    patient_type: Optional[str] = None,
    teleconsult: Optional[bool] = None,
    verified_only: bool = False,
    min_rating: float = 0,
    min_experience: int = 0,
):
    results = []
    for d in DOCTORS:
        if hmo and hmo not in d["hmos"]:
            continue
        if specialty and d["specialty"] != specialty:
            continue
        if location and d["location"] != location:
            continue
        if patient_type and patient_type not in d["patient_types"]:
            continue
        if teleconsult is True and not d["teleconsult"]:
            continue
        if verified_only and not d["verified"]:
            continue
        if d["rating"] < min_rating:
            continue
        if d["experience_years"] < min_experience:
            continue
        results.append(d)
    return {"count": len(results), "items": results}

@app.get("/doctors/{doctor_id}")
def doctor_detail(doctor_id: int):
    doctor = next((d for d in DOCTORS if d["id"] == doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/appointments", status_code=201)
def create_appointment(payload: AppointmentCreate):
    doctor = next((d for d in DOCTORS if d["id"] == payload.doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if payload.hmo_provider not in doctor["hmos"]:
        raise HTTPException(status_code=409, detail="Selected HMO is not listed for this doctor in the demo directory.")
    appointment = {
        "id": str(uuid.uuid4()),
        **payload.model_dump(),
        "doctor_name": doctor["name"],
        "clinic": doctor["clinic"],
        "status": "pending_verification",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    APPOINTMENTS.append(appointment)
    return appointment

@app.get("/appointments")
def list_appointments():
    return {"count": len(APPOINTMENTS), "items": APPOINTMENTS}
