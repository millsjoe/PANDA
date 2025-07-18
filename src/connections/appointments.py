from .base import BaseConnection


class AppointmentsConnection(BaseConnection):
    def __init__(self):
        super().__init__()

    def get_appointments(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM appointments")
            rows = cursor.fetchall()

            appointments = []
            for row in rows:
                appointment = {
                    "id": str(row[0]),
                    "patient_nhs_number": row[1],
                    "status": row[2],
                    "appointment_time": str(row[3]) if row[3] else None,
                    "duration": row[4],
                    "clinician": row[5],
                    "department": row[6],
                    "postcode": row[7],
                }
                appointments.append(appointment)

            return appointments
