from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.connections.appointments import AppointmentsConnection

router = APIRouter()


@router.get(
    "/api/appointments",
    summary="Get all appointments",
    description="Returns a list of all appointments from the database.",
    response_description="A list of appointment objects.",
    tags=["appointments"],
    responses={
        200: {
            "description": "A list of appointment objects.",
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
        },
        500: {
            "description": "Failed to fetch appointments",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Failed to fetch appointments",
                        "detail": "Connection to database failed",
                    }
                },
            },
        },
    },
)
def get_appointments():
    try:
        appointments_connection = AppointmentsConnection()
        appointments = appointments_connection.get_appointments()
        appointments_connection.close_connection()
        return JSONResponse(content=appointments, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to fetch appointments", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
