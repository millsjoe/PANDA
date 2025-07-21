from pydantic import BaseModel

# TODO: add clinician model
class Patient(BaseModel):
    nhs_number: str
    name: str
    date_of_birth: str
    postcode: str


class Appointment(BaseModel):
    patient_nhs_number: str
    status: str
    appointment_time: str
    duration: str
    clinician: str
    department: str
    postcode: str
    id: str
