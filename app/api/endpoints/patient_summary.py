from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.crud import patient_details, patient_symptoms, patient_visits, doctor
from app.api.deps import get_db
from app.db.schemas.patient import Patient
from app.db.schemas.patient_symptoms import PatientSymptom
from app.db.schemas.patient_visits import PatientVisit
from app.db.schemas.doctor import Doctor
from app.db.schemas.patient_summary import PatientSummaryResponse, VisitDetails

router = APIRouter(prefix="/patient_summary", tags=["patient_summary"])


@router.get("/{patient_id}/summary", response_model=PatientSummaryResponse)
def get_patient_summary(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve detailed summary for a patient including visits, symptoms, and doctor details.
    """
    patient = patient_details.get_patient_details(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    symptoms = patient_symptoms.get_patient_symptoms_by_patient_id(db, patient_id)

    visit_details = []

    for symptom in symptoms:
        visits = patient_visits.get_patient_visits_by_symptom_id(db, symptom.SymptomID)

        for visit in visits:
            doctor_data = doctor.get_doctor(db, visit.DoctorID)

            visit_details.append(VisitDetails(visit=visit, symptoms=[symptom], doctor=doctor_data))

    return PatientSummaryResponse(patient=patient, visits=visit_details)