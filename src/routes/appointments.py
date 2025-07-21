from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.connections.appointments import AppointmentsConnection
from src.models import Appointment

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
        if not appointments:
            return JSONResponse(
                content={"error": "No appointments found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(content=appointments, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to fetch appointments", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/api/appointments/{id}",
    summary="Get an appointment by ID",
    description="Returns an appointment by ID from the database.",
    response_description="An appointment object.",
    tags=["appointments"],
)
def get_appointment(id: str):
    try:
        appointments_connection = AppointmentsConnection()
        appointment = appointments_connection.get_appointment(id)
        appointments_connection.close_connection()
        if not appointment:
            return JSONResponse(
                content={"error": "No appointment found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(content=appointment, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to fetch appointment", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/api/appointments/patient/{patient_nhs_number}",
    summary="Get appointments by patient NHS number",
    description="Returns a list of appointments by patient NHS number from the database.",
    response_description="A list of appointment objects.",
    tags=["appointments"],
    responses={
        200: {
            "description": "A list of appointment objects.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "patient_nhs_number": "1234567890",
                            "status": "confirmed",
                            "appointment_time": "2021-01-01T00:00:00",
                            "duration": "30",
                            "clinician": "Dr. John Doe",
                            "department": "Cardiology",
                            "postcode": "SW1A 1AA",
                            "id": "1234567890",
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
                }
            },
        },
    },
)
def get_appointments_by_patient_nhs_number(patient_nhs_number: str):
    try:
        appointments_connection = AppointmentsConnection()
        appointments = appointments_connection.get_appointments_by_patient_nhs_number(
            patient_nhs_number
        )
        appointments_connection.close_connection()
        if not appointments:
            return JSONResponse(
                content={"error": "No appointments found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return JSONResponse(content=appointments, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to fetch appointments", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post(
    "/api/appointments",
    summary="Create an appointment",
    description="Creates an appointment in the database.",
    response_description="An appointment object.",
    tags=["appointments"],
    responses={
        201: {
            "description": "Appointment created",
            "content": {
                "application/json": {"example": {"message": "Appointment created"}}
            },
        },
        500: {
            "description": "Failed to create appointment",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Failed to create appointment",
                        "detail": "Connection to database failed",
                    }
                }
            },
        },
    },
)
def create_appointment(appointment: Appointment):
    try:
        appointments_connection = AppointmentsConnection()
        appointments_connection.create_appointment(appointment)
        appointments_connection.close_connection()
        return JSONResponse(
            content={"message": "Appointment created"},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to create appointment", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put(
    "/api/appointments/{id}",
    summary="Update an appointment",
    description="Updates an appointment in the database.",
    response_description="An appointment object.",
    tags=["appointments"],
    responses={
        200: {
            "description": "Appointment updated",
            "content": {
                "application/json": {"example": {"message": "Appointment updated"}}
            },
        },
        500: {
            "description": "Failed to update appointment",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Failed to update appointment",
                        "detail": "Connection to database failed",
                    }
                }
            },
        },
    },
)
def update_appointment(appointment: Appointment):
    try:
        appointments_connection = AppointmentsConnection()
        appointments_connection.update_appointment(appointment)
        appointments_connection.close_connection()
        return JSONResponse(
            content={"message": "Appointment updated"}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to update appointment", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete(
    "/api/appointments/{id}",
    summary="Delete an appointment",
    description="Deletes an appointment from the database.",
    response_description="An appointment object.",
    tags=["appointments"],
    responses={
        200: {
            "description": "Appointment deleted",
            "content": {
                "application/json": {"example": {"message": "Appointment deleted"}}
            },
        },
        500: {
            "description": "Failed to delete appointment",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Failed to delete appointment",
                        "detail": "Connection to database failed",
                    }
                }
            },
        },
    },
)
def delete_appointment(id: str):
    try:
        appointments_connection = AppointmentsConnection()
        appointments_connection.delete_appointment(id)
        appointments_connection.close_connection()
        return JSONResponse(
            content={"message": "Appointment deleted"}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"error": "Failed to delete appointment", "detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
