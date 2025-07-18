from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from connections.patients import PatientsConnection

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
            "content": {
                "application/json": {
                    "example": [
                        {
                            "nhs_number": "1234567890",
                            "name": "John Doe",
                            "date_of_birth": "1990-01-01",
                            "postcode": "SW1A 1AA",
                        }
                    ]
                }
            },
        }
    },
)
def get_patients():
    try:
        patients_connection = PatientsConnection()
        patients = patients_connection.get_patients()
        patients_connection.close_connection()
        return JSONResponse(content=patients, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to fetch patients", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/api/patients/{nhs_number}",
    summary="Get a patient by NHS number",
    description="Returns a patient by NHS number from the database.",
    response_description="A patient object.",
    tags=["patients"],
    responses={
        200: {
            "description": "A patient object.",
            "content": {
                "application/json": {
                    "example": {
                        "nhs_number": "1234567890",
                        "name": "John Doe",
                        "date_of_birth": "1990-01-01",
                        "postcode": "SW1A 1AA",
                    }
                }
            },
        },
        404: {
            "description": "Patient not found",
            "content": {
                "application/json": {"example": {"error": "Patient not found"}}
            },
        },
    },
)
def get_patient(nhs_number: str):
    try:
        patients_connection = PatientsConnection()
        patient = patients_connection.get_patient_by_nhs_number(nhs_number)
        patients_connection.close_connection()

        if not patient:
            return JSONResponse(
                content={"error": f"Patient with NHS number {nhs_number} not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return JSONResponse(content=patient, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to fetch patient", "detail": str(e)},
            status_code=status.HTTP_404_NOT_FOUND,
        )
