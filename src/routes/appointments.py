import json
import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/appointments")
def get_appointments():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # to remove when using db
    json_path = os.path.join(current_dir, "..", "..", "example_appointments.json")
    with open(json_path, "r") as f:
        return json.load(f)