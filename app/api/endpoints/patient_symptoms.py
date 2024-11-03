# app/api/endpoints/patient_symptoms.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.crud import patient_symptoms as patient_symptom_crud
from app.db.schemas.patient_symptoms import PatientSymptom, PatientSymptomCreate, PatientSymptomUpdate
from app.api.deps import get_db

router = APIRouter(prefix="/patient_symptoms", tags=["patient_symptoms"])

@router.post("/", response_model=PatientSymptom, status_code=201)
def create_patient_symptom(patient_symptom: PatientSymptomCreate, db: Session = Depends(get_db)):
    """
    Create a new patient symptom record.
    """
    return patient_symptom_crud.create_patient_symptom(db=db, patient_symptom=patient_symptom)

@router.get("/", response_model=List[PatientSymptom])
def read_patient_symptoms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all patient symptoms.
    """
    return patient_symptom_crud.get_all_patient_symptoms(db, skip=skip, limit=limit)

@router.get("/{symptom_id}", response_model=PatientSymptom)
def read_patient_symptom(symptom_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a patient symptom by ID.
    """
    db_symptom = patient_symptom_crud.get_patient_symptom(db, symptom_id=symptom_id)
    return db_symptom

@router.put("/{symptom_id}", response_model=PatientSymptom)
def update_patient_symptom(symptom_id: int, patient_symptom: PatientSymptomUpdate, db: Session = Depends(get_db)):
    """
    Update an existing patient symptom record.
    """
    db_symptom = patient_symptom_crud.update_patient_symptom(db=db, symptom_id=symptom_id, patient_symptom=patient_symptom)
    return db_symptom

@router.delete("/{symptom_id}", status_code=204)
def delete_patient_symptom(symptom_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient symptom by ID.
    """
    patient_symptom_crud.delete_patient_symptom(db=db, symptom_id=symptom_id)
    return None
