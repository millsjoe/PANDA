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
    def setup_mocks(self, mock_psycopg2):
        """Setup mocks for all tests in this class"""
        self.mock_conn = mock_psycopg2.return_value
        self.mock_cursor = Mock()

        self.mock_cursor.__enter__ = Mock(return_value=self.mock_cursor)
        self.mock_cursor.__exit__ = Mock(return_value=None)
        self.mock_conn.cursor = Mock(return_value=self.mock_cursor)

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
