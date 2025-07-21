from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routes.patients import router as patients_router
import pytest
from unittest.mock import Mock, patch

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

app = FastAPI()
app.include_router(patients_router)
client = TestClient(app)


class TestPatientsRoute:
    """Tests for PatientsRoute class"""

    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_psycopg2):
        """Setup mocks for all tests in this class"""
        self.mock_conn = mock_psycopg2.return_value
        self.mock_cursor = Mock()

        self.mock_cursor.__enter__ = Mock(return_value=self.mock_cursor)
        self.mock_cursor.__exit__ = Mock(return_value=None)
        self.mock_conn.cursor = Mock(return_value=self.mock_cursor)

    def test_get_patients_success(self):
        """GET /api/patients returns a list of patients"""
        self.mock_cursor.fetchall.return_value = [
            ("1234567890", "John Doe", "1990-01-01", "SW1A 1AA"),
            ("1234567891", "Jane Smith", "1991-02-02", "SW1A 1AB"),
        ]

        response = client.get("/api/patients")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["nhs_number"] == "1234567890"

    def test_get_patient_by_nhs_number_success(self):
        """GET /api/patients/{nhs_number} returns a patient"""
        self.mock_cursor.fetchone.return_value = (
            "1234567890",
            "John Doe",
            "1990-01-01",
            "SW1A 1AA",
        )
        response = client.get("/api/patients/1234567890")
        assert response.status_code == 200
        data = response.json()
        assert data["nhs_number"] == "1234567890"
        assert data["name"] == "John Doe"
        assert data["date_of_birth"] == "1990-01-01"
        assert data["postcode"] == "SW1A 1AA"

    def test_get_patient_by_nhs_number_not_found(self):
        """GET /api/patients/{nhs_number} returns 404 for non-existent patient"""
        self.mock_cursor.fetchone.return_value = None
        response = client.get("/api/patients/9999999999")
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "Patient with NHS number 9999999999 not found"
