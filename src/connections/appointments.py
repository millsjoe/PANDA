from .base import BaseConnection
from src.models import Appointment

# TODO: add missed appointment handling
# TODO: handle timezones


class AppointmentsConnection(BaseConnection):
    def __init__(self):
        super().__init__()

    def get_appointments(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute(
                "SELECT patient_nhs_number, status, time, duration, clinician, department, postcode, id FROM appointments"
            )
            rows = cursor.fetchall()

            appointments = []
            for row in rows:
                appointment = {
                    "patient_nhs_number": str(row[0]),
                    "status": str(row[1]),
                    "appointment_time": str(row[2]),
                    "duration": str(row[3]),
                    "clinician": str(row[4]),
                    "department": str(row[5]),
                    "postcode": str(row[6]),
                    "id": str(row[7]),
                }
                appointments.append(appointment)

            return appointments

    def get_appointment(self, id: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute(
                "SELECT patient_nhs_number, status, time, duration, clinician, department, postcode, id FROM appointments WHERE id = %s",
                (id,),
            )
            row = cursor.fetchone()

            if row:

                return {
                    "patient_nhs_number": str(row[0]),
                    "status": str(row[1]),
                    "appointment_time": str(row[2]),
                    "duration": str(row[3]),
                    "clinician": str(row[4]),
                    "department": str(row[5]),
                    "postcode": str(row[6]),
                    "id": str(row[7]),
                }

    def get_appointments_by_patient_nhs_number(self, patient_nhs_number: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute(
                "SELECT patient_nhs_number, status, time, duration, clinician, department, postcode, id FROM appointments WHERE patient_nhs_number = %s",
                (patient_nhs_number,),
            )
            rows = cursor.fetchall()
            if rows:
                appointments = []
                for row in rows:
                    appointment = {
                        "patient_nhs_number": str(row[0]),
                        "status": str(row[1]),
                        "appointment_time": str(row[2]),
                        "duration": str(row[3]),
                        "clinician": str(row[4]),
                        "department": str(row[5]),
                        "postcode": str(row[6]),
                        "id": str(row[7]),
                    }
                    appointments.append(appointment)
                return appointments
            return None

    def create_appointment(self, appointment: Appointment):
        with self.get_connection().cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO appointments (patient_nhs_number, status, appointment_time, duration, clinician, department, postcode, id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        appointment.patient_nhs_number,
                        appointment.status,
                        appointment.appointment_time,
                        appointment.duration,
                        appointment.clinician,
                        appointment.department,
                        appointment.postcode,
                        appointment.id,
                    ),
                )
                self.get_connection().commit()
                return True
            except Exception as e:
                raise e

    def update_appointment(self, appointment: Appointment):
        with self.get_connection().cursor() as cursor:
            try:

                cursor.execute(
                    "UPDATE appointments SET status = %s, appointment_time = %s, duration = %s, clinician = %s, department = %s, postcode = %s WHERE id = %s",
                    (
                        appointment.status,
                        appointment.appointment_time,
                        appointment.duration,
                        appointment.clinician,
                        appointment.department,
                        appointment.postcode,
                        appointment.id,
                    ),
                )
                self.get_connection().commit()
                return True

            except Exception as e:
                raise e

    def delete_appointment(self, id: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute("DELETE FROM appointments WHERE id = %s", (id,))
            self.get_connection().commit()
