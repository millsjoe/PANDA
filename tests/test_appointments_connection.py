import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.connections.appointments import AppointmentsConnection
from unittest.mock import Mock


class TestAppointmentsConnection:
    """Tests for AppointmentsConnection class"""

    def test_get_appointments_returns_list_of_appointments(self, mock_psycopg2):
        """get_appointments returns a list of appointments"""
        mock_conn = mock_psycopg2.return_value

        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
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

        mock_cursor.__enter__ = Mock(
            return_value=mock_cursor
        )  # needed for context manager
        mock_cursor.__exit__ = Mock(return_value=None)

        mock_conn.cursor = Mock(return_value=mock_cursor)  # needed for context manager

        connection = AppointmentsConnection()
        result = connection.get_appointments()

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(appointment, dict) for appointment in result)
        assert all("patient_nhs_number" in appointment for appointment in result)
        assert all("status" in appointment for appointment in result)
        assert all("appointment_time" in appointment for appointment in result)
        assert all("duration" in appointment for appointment in result)
        assert all("clinician" in appointment for appointment in result)
        assert all("department" in appointment for appointment in result)
        assert all("postcode" in appointment for appointment in result)
        assert all("id" in appointment for appointment in result)
