import json
import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/appointments",
    summary="Get all appointments",
    description="Returns a list of all appointments from the database.",
    response_description="A list of appointment objects.",
    tags=["appointments"],
    responses={
        200: {
            "description": "A list of appointment objects.",
            "content": {"application/json": {"example": [{"nhs_number": "1234567890", "name": "John Doe", "date_of_birth": "1990-01-01", "postcode": "SW1A 1AA"}]}}
        }
    }
)
def get_appointments():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # to remove when using db
    json_path = os.path.join(current_dir, "..", "..", "example_appointments.json")
    with open(json_path, "r") as f:
        return json.load(f)