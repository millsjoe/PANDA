import json
import os
import psycopg2


## only intended to be used once to populate the database
conn = psycopg2.connect(
    host="db", database="panda_db", user="postgres", password=os.getenv("DB_PASSWORD")
)


with conn.cursor() as cur:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            nhs_number VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255),
            date_of_birth DATE,
            postcode VARCHAR(10)
        );
        
        CREATE TABLE IF NOT EXISTS appointments (
            id VARCHAR(36) PRIMARY KEY,
            patient_nhs_number VARCHAR(10) REFERENCES patients(nhs_number),
            status VARCHAR(20),
            time TIMESTAMP,
            duration VARCHAR(10),
            clinician VARCHAR(255),
            department VARCHAR(50),
            postcode VARCHAR(10)
        );
    """
    )
    conn.commit()


with open("example_patients.json") as f:
    patients = json.load(f)

with open("example_appointments.json") as f:
    appointments = json.load(f)

with conn.cursor() as cur:
    for patient in patients:
        cur.execute(
            """
            INSERT INTO patients VALUES (%s, %s, %s, %s)
            ON CONFLICT (nhs_number) DO NOTHING
        """,
            (
                patient["nhs_number"],
                patient["name"],
                patient["date_of_birth"],
                patient["postcode"],
            ),
        )

    for apt in appointments:
        cur.execute(
            """
            INSERT INTO appointments VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """,
            (
                apt["id"],
                apt["patient"],
                apt["status"],
                apt["time"],
                apt["duration"],
                apt["clinician"],
                apt["department"],
                apt["postcode"],
            ),
        )

    conn.commit()

print(f"Inserted {len(patients)} patients and {len(appointments)} appointments")
conn.close()
