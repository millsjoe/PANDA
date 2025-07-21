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
                    "patient_nhs_number": str(row[0]),
                    "status": row[1],
                    "appointment_time": str(row[2]) if row[2] else None,
                    "duration": row[3],
                    "clinician": row[4],
                    "department": row[5],
                    "postcode": row[6],
                    "id": str(row[7]),
                }
                appointments.append(appointment)

            return appointments
