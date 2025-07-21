import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.connections.appointments import AppointmentsConnection
from src.models import Appointment
from unittest.mock import Mock


class TestAppointmentsConnection:
    """Tests for AppointmentsConnection class"""

    def test_get_appointments_returns_list_of_appointments(self, mock_db_connection):
        """get_appointments returns a list of appointments"""
        mock_cursor = mock_db_connection

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

    def test_get_appointment_by_patient_nhs_number_returns_list_of_appointments(
        self, mock_db_connection
    ):
        """get_appointment_by_patient_nhs_number returns a list of appointments"""
        mock_cursor = mock_db_connection

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

        connection = AppointmentsConnection()
        result = connection.get_appointments_by_patient_nhs_number("1953262716")

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

    def test_get_appointment_by_id_returns_appointment(self, mock_db_connection):
        """get_appointment_by_id returns an appointment"""
        mock_cursor = mock_db_connection

        mock_cursor.fetchone.return_value = (
            "1953262716",
            "active",
            "2025-06-04T16:30:00+01:00",
            "1h",
            "Bethany Rice-Hammond",
            "oncology",
            "IM2N 4LG",
            "01542f70-929f-4c9a-b4fa-e672310d7e78",
        )

        connection = AppointmentsConnection()
        result = connection.get_appointment("01542f70-929f-4c9a-b4fa-e672310d7e78")

        assert isinstance(result, dict)
        assert "patient_nhs_number" in result
        assert "status" in result
        assert "appointment_time" in result
        assert "duration" in result
        assert "clinician" in result
        assert "department" in result
        assert "postcode" in result
        assert "id" in result

    def test_create_appointment_success(self, mock_db_connection):
        """create_appointment returns True"""
        mock_cursor = mock_db_connection

        connection = AppointmentsConnection()
        assert connection.create_appointment(
            Appointment(
                patient_nhs_number="1953262716",
                status="active",
                appointment_time="2025-06-04T16:30:00+01:00",
                duration="1h",
                clinician="Bethany Rice-Hammond",
                department="oncology",
                postcode="IM2N 4LG",
                id="01542f70-929f-4c9a-b4fa-e672310d7e78",
            )
        )

    def test_update_appointment_success(self, mock_db_connection):
        """update_appointment returns True"""

        connection = AppointmentsConnection()
        assert connection.update_appointment(
            Appointment(
                patient_nhs_number="1953262716",
                status="active",
                appointment_time="2025-06-04T16:30:00+01:00",
                duration="1h",
                clinician="Bethany Rice-Hammond",
                department="oncology",
                postcode="IM2N 4LG",
                id="01542f70-929f-4c9a-b4fa-e672310d7e78",
            )
        )
