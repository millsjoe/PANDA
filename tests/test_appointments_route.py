from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routes.appointments import router as appointments_router
import pytest
from unittest.mock import Mock, patch

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

app = FastAPI()
app.include_router(appointments_router)
client = TestClient(app)


class TestAppointmentsRoute:
    """Tests for AppointmentsRoute class"""

    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_db_connection):
        """Setup mocks for all tests in this class"""
        self.mock_cursor = mock_db_connection

    def test_get_appointments_success(self):
        """GET /api/appointments returns a list of appointments"""
        self.mock_cursor.fetchall.return_value = [
            (
                "1953262716",
                "active",
                "2025-06-04T16:30:00+01:00",
                "1h",
                "Bethany Rice-Hammond",
                "oncology",
                "IM2N 4LG",
                "01542f70-929f-4c9a-b4fa-e672310d7e78",
            ),
            (
                "1953262717",
                "active",
                "2025-06-04T17:30:00+01:00",
                "1h",
                "John Doe",
                "oncology",
                "IM3N 5LG",
                "01542f70-929f-4c9a-b4fa-e672310d7e79",
            ),
        ]

        response = client.get("/api/appointments")
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert data[0]["patient_nhs_number"] == "1953262716"
        assert data[0]["status"] == "active"
        assert data[0]["appointment_time"] == "2025-06-04T16:30:00+01:00"
        assert data[0]["duration"] == "1h"
        assert data[0]["clinician"] == "Bethany Rice-Hammond"
        assert data[0]["department"] == "oncology"
        assert data[0]["postcode"] == "IM2N 4LG"
        assert data[0]["id"] == "01542f70-929f-4c9a-b4fa-e672310d7e78"

    def test_get_appointment_by_id_success(self):
        """GET /api/appointments/{id} returns an appointment"""
        self.mock_cursor.fetchone.return_value = (
            "1953262716",
            "active",
            "2025-06-04T16:30:00+01:00",
            "1h",
            "Bethany Rice-Hammond",
            "oncology",
            "IM2N 4LG",
            "01542f70-929f-4c9a-b4fa-e672310d7e78",
        )

        response = client.get("/api/appointments/01542f70-929f-4c9a-b4fa-e672310d7e78")
        assert response.status_code == 200
        data = response.json()

        assert data["patient_nhs_number"] == "1953262716"
        assert data["status"] == "active"
        assert data["appointment_time"] == "2025-06-04T16:30:00+01:00"
        assert data["duration"] == "1h"
        assert data["clinician"] == "Bethany Rice-Hammond"
        assert data["department"] == "oncology"
        assert data["postcode"] == "IM2N 4LG"
        assert data["id"] == "01542f70-929f-4c9a-b4fa-e672310d7e78"

    def test_get_appointments_by_patient_nhs_number_success(self):
        """GET /api/appointments/patient/{patient_nhs_number} returns a list of appointments"""
        self.mock_cursor.fetchall.return_value = [
            (
                "1953262716",
                "active",
                "2025-06-04T16:30:00+01:00",
                "1h",
                "Bethany Rice-Hammond",
                "oncology",
                "IM2N 4LG",
                "01542f70-929f-4c9a-b4fa-e672310d7e78",
            ),
        ]

        response = client.get("/api/appointments/patient/1953262716")
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["patient_nhs_number"] == "1953262716"
        assert data[0]["status"] == "active"
        assert data[0]["appointment_time"] == "2025-06-04T16:30:00+01:00"
        assert data[0]["duration"] == "1h"
        assert data[0]["clinician"] == "Bethany Rice-Hammond"
        assert data[0]["department"] == "oncology"
        assert data[0]["postcode"] == "IM2N 4LG"
        assert data[0]["id"] == "01542f70-929f-4c9a-b4fa-e672310d7e78"

    def test_create_appointment_success(self):
        """POST /api/appointments creates an appointment"""
        response = client.post(
            "/api/appointments",
            json={
                "patient_nhs_number": "1953262716",
                "status": "active",
                "appointment_time": "2025-06-04T16:30:00+01:00",
                "duration": "1h",
                "clinician": "Bethany Rice-Hammond",
                "department": "oncology",
                "postcode": "IM2N 4LG",
                "id": "01542f70-929f-4c9a-b4fa-e672310d7e78",
            },
        )
        assert response.status_code == 201
        data = response.json()

        assert data["message"] == "Appointment created"

    def test_update_appointment_success(self):
        """PUT /api/appointments/{id} updates an appointment"""
        response = client.put(
            "/api/appointments/01542f70-929f-4c9a-b4fa-e672310d7e78",
            json={
                "patient_nhs_number": "1953262716",
                "status": "cancelled",
                "appointment_time": "2025-06-04T16:30:00+01:00",
                "duration": "1h",
                "clinician": "Bethany Rice-Hammond",
                "department": "oncology",
                "postcode": "IM2N 4LG",
                "id": "01542f70-929f-4c9a-b4fa-e672310d7e78",
            },
        )
        assert response.status_code == 200
        data = response.json()

        assert data["message"] == "Appointment updated"

    def test_delete_appointment_success(self):
        """DELETE /api/appointments/{id} deletes an appointment"""
        response = client.delete(
            "/api/appointments/01542f70-929f-4c9a-b4fa-e672310d7e78"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Appointment deleted"
