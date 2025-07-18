import json
import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/patients")
def get_patients():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # to remove when using db
    json_path = os.path.join(current_dir, "..", "..", "example_patients.json")
    with open(json_path, "r") as f:
        return json.load(f)

@router.get("/api/patients/{nhs_number}")
def get_patient(nhs_number: str):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # to remove when using db
    json_path = os.path.join(current_dir, "..", "..", "example_patients.json")
    with open(json_path, "r") as f:
        patients = json.load(f)
        for patient in patients:
            if patient["nhs_number"] == nhs_number:
                return patient
    return {"error": "Patient not found"}