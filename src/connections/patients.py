from .base import BaseConnection
from src.models import Patient
from src.utils.checksum import calculate_checksum


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
                    "date_of_birth": str(row[2]),
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

    def create_patient(self, patient: Patient):
        if not calculate_checksum(patient.nhs_number):
            raise ValueError("Invalid NHS number")

        with self.get_connection().cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO patients (nhs_number, name, date_of_birth, postcode) VALUES (%s, %s, %s, %s)",
                    (
                        patient.nhs_number,
                        patient.name,
                        patient.date_of_birth,
                        patient.postcode,
                    ),
                )
                self.get_connection().commit()
                return True
            except Exception as e:
                raise e

    def update_patient(self, patient: Patient):
        with self.get_connection().cursor() as cursor:
            try:
                cursor.execute(
                    "UPDATE patients SET name = %s, date_of_birth = %s, postcode = %s WHERE nhs_number = %s",
                    (
                        patient.name,
                        patient.date_of_birth,
                        patient.postcode,
                        patient.nhs_number,
                    ),
                )
                self.get_connection().commit()
                return True
            except Exception as e:
                raise e
