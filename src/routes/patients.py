import json
import os
from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/api/patients",
    summary="Get all patients",
    description="Returns a list of all patients database.",
    response_description="A list of patient objects.",
    tags=["patients"],
    responses={
        200: {
            "description": "A list of patient objects.",
            "content": {"application/json": {"example": [{"nhs_number": "1234567890", "name": "John Doe", "date_of_birth": "1990-01-01", "postcode": "SW1A 1AA"}]}}
        }
    }
)
def get_patients():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # to remove when using db
    json_path = os.path.join(current_dir, "..", "..", "example_patients.json")
    with open(json_path, "r") as f:
        return json.load(f)

@router.get("/api/patients/{nhs_number}",
    summary="Get a patient by NHS number",
    description="Returns a patient by NHS number from the database.",
    response_description="A patient object.",
    tags=["patients"],
    responses={
        200: {
            "description": "A patient object.",
            "content": {"application/json": {"example": {"nhs_number": "1234567890", "name": "John Doe", "date_of_birth": "1990-01-01", "postcode": "SW1A 1AA"}}}
        },
        404: {
            "description": "Patient not found",
            "content": {"application/json": {"example": {"error": "Patient not found"}}}
        }
    }
)
def get_patient(nhs_number: str):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # to remove when using db
    json_path = os.path.join(current_dir, "..", "..", "example_patients.json")
    with open(json_path, "r") as f:
        patients = json.load(f)
        for patient in patients:
            if patient["nhs_number"] == nhs_number:
                return patient
    return {"error": "Patient not found"}