import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.connections.patients import PatientsConnection
from unittest.mock import Mock


class TestPatientsConnection:
    """Tests for PatientsConnection class"""

    def test_get_patients_returns_list_of_patients(self, mock_psycopg2):
        """get_patients returns a list of patients"""
        mock_conn = mock_psycopg2.return_value

        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ("1234567890", "John Doe", "1990-01-01", "1234567890"),
            ("1234567891", "Jane Smith", "1991-02-02", "1234567891"),
            ("1234567892", "Jim Beam", "1992-03-03", "1234567892"),
        ]

        mock_cursor.__enter__ = Mock(
            return_value=mock_cursor
        )  # needed for context manager
        mock_cursor.__exit__ = Mock(return_value=None)

        mock_conn.cursor = Mock(return_value=mock_cursor)  # needed for context manager

        connection = PatientsConnection()

        result = connection.get_patients()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(patient, dict) for patient in result)
        assert all("nhs_number" in patient for patient in result)
        assert all("name" in patient for patient in result)
        assert all("date_of_birth" in patient for patient in result)
        assert all("postcode" in patient for patient in result)

    def test_get_patient_by_nhs_number_returns_patient(self, mock_psycopg2):
        """get_patient_by_nhs_number returns a patient"""
        mock_conn = mock_psycopg2.return_value

        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (
            "1234567890",
            "John Doe",
            "1990-01-01",
            "1234567890",
        )

        mock_cursor.__enter__ = Mock(
            return_value=mock_cursor
        )  # needed for context manager
        mock_cursor.__exit__ = Mock(return_value=None)

        mock_conn.cursor = Mock(return_value=mock_cursor)  # needed for context manager

        connection = PatientsConnection()
        result = connection.get_patient_by_nhs_number("1234567890")

        assert isinstance(result, dict)
        assert result["nhs_number"] == "1234567890"
        assert result["name"] == "John Doe"
        assert result["date_of_birth"] == "1990-01-01"
        assert result["postcode"] == "1234567890"
