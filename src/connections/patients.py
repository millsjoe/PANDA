from .base import BaseConnection


class PatientsConnection(BaseConnection):
    def __init__(self):
        super().__init__()

    def get_patients(self):
        with self.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()

            patients = []
            for row in rows:
                patient = {
                    "nhs_number": row[0],
                    "name": row[1],
                    "date_of_birth": str(row[2]) if row[2] else None,
                    "postcode": row[3],
                }
                patients.append(patient)

            return patients

    def get_patient_by_nhs_number(self, nhs_number: str):
        with self.get_connection().cursor() as cursor:
            cursor.execute(
                "SELECT * FROM patients WHERE nhs_number = %s", (nhs_number,)
            )
            row = cursor.fetchone()

            if row:
                return {
                    "nhs_number": row[0],
                    "name": row[1],
                    "date_of_birth": str(row[2]) if row[2] else None,
                    "postcode": row[3],
                }
            return None
