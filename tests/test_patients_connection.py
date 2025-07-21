import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.connections.patients import PatientsConnection
from unittest.mock import Mock
from src.models import Patient


class TestPatientsConnection:
    """Tests for PatientsConnection class"""

    def test_get_patients_returns_list_of_patients(self, mock_db_connection):
        """get_patients returns a list of patients"""
        mock_cursor = mock_db_connection

        mock_cursor.fetchall.return_value = [
            ("1234567890", "John Doe", "1990-01-01", "1234567890"),
            ("1234567891", "Jane Smith", "1991-02-02", "1234567891"),
            ("1234567892", "Jim Beam", "1992-03-03", "1234567892"),
        ]

        connection = PatientsConnection()

        result = connection.get_patients()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(patient, dict) for patient in result)
        assert all("nhs_number" in patient for patient in result)
        assert all("name" in patient for patient in result)
        assert all("date_of_birth" in patient for patient in result)
        assert all("postcode" in patient for patient in result)

    def test_get_patient_by_nhs_number_returns_patient(self, mock_db_connection):
        """get_patient_by_nhs_number returns a patient"""
        mock_cursor = mock_db_connection

        mock_cursor.fetchone.return_value = (
            "1234567890",
            "John Doe",
            "1990-01-01",
            "1234567890",
        )

        connection = PatientsConnection()
        result = connection.get_patient_by_nhs_number("1234567890")

        assert isinstance(result, dict)
        assert result["nhs_number"] == "1234567890"
        assert result["name"] == "John Doe"
        assert result["date_of_birth"] == "1990-01-01"
        assert result["postcode"] == "1234567890"

    def test_create_patient_success(self, mock_db_connection):
        """create_patient returns True"""
        mock_cursor = mock_db_connection

        connection = PatientsConnection()
        assert connection.create_patient(
            Patient(
                nhs_number="0021403597",
                name="John Doe",
                date_of_birth="1990-01-01",
                postcode="1234567890",
            )
        )

    def test_create_patient_failure(self, mock_db_connection):
        """create_patient raises error if bad data is provided"""
        mock_cursor = mock_db_connection

        connection = PatientsConnection()
        with pytest.raises(ValueError):
            connection.create_patient(
                Patient(
                    nhs_number="12346",  # invalid NHS number
                    name="John Doe",
                    date_of_birth="1990-01-01",
                    postcode="1234567890",
                )
            )

    def test_update_patient_success(self, mock_db_connection):
        """update_patient returns True"""
        mock_cursor = mock_db_connection

        connection = PatientsConnection()
        assert connection.update_patient(
            Patient(
                nhs_number="0021403597",
                name="John Doe",
                date_of_birth="1990-01-01",
                postcode="1234567890",
            )
        )

    def test_update_patient_failure(self, mock_db_connection):
        """update_patient raises error if bad data is provided"""

        connection = PatientsConnection()
        with pytest.raises(ValueError):
            connection.update_patient(
                Patient(
                    nhs_number="1245",  # invalid NHS number
                    name=1234,  # type: ignore bad data
                    date_of_birth="1990-01-01",
                    postcode="1234567890",
                )
            )
