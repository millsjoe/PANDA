# PANDA 
> REQUIRES ENV DB_PASSWORD TO RUN - please reach out if you need it 
## What is it?
PANDA is an **MVP** for a Patient Appointment Network Data Application

## Considerations
As this was an MVP done in ~2.5 hours I have chosen to prioritise the following requirements: 
- CRUD capabilities
- Error propegation 
- Documentation
- Unit tests 
- Docker based for reduced lock in and easily deployable

Therefore there are some requirements not implemented such as: 
- Postcode formatting
- Handling of missed appointments 
- Timezone awareness

Where consideration have been made they are marked in code by:
> TODO - add x implementation to y

## Tech Choices 
- **Python**: This is a python role, i think would be daft to not consider that especially given its capability for a backend service like this
- **FastAPI**: lightning fast API service that rivals Node & Go. Whilst also containing easily documentable API routes via Swagger integration
- **MyPy**: Extra layer of type safety
- **Pydantic**: A way to model data types
- **Pytest**: Capabilitues of testing with common techniques such as mocking, fixtures etc
- **Postgresql**: Though a trivial dataset they are relational so better option than nosql. Plus, adds room to expand with things like clinician later on. Great integrations with docker too
- **Docker**: Docker is a great way to ensure cross compatibility and ease of deployment - not being locked to a specific vendor

## Schema 


### Patient
| Column Name     | Type         | Nullable | Description                    |
| --------------- | ------------ | -------- | ------------------------------ |
| `nhs_number`    | VARCHAR(10)  | No       | Primary key. Unique NHS number |
| `name`          | VARCHAR(255) | Yes      | Full patient name              |
| `date_of_birth` | DATE         | Yes      | Patient’s date of birth        |
| `postcode`      | VARCHAR(10)  | Yes      | Patient’s postcode             |

### Appointment
| Column Name          | Type         | Nullable | Description                                    |
| -------------------- | ------------ | -------- | ---------------------------------------------- |
| `id`                 | VARCHAR(36)  | No       | Primary key (UUID or similar)                  |
| `patient_nhs_number` | VARCHAR(10)  | No       | FK → `patients.nhs_number`                     |
| `status`             | VARCHAR(20)  | Yes      | Appointment status (e.g. scheduled, cancelled) |
| `time`               | TIMESTAMP    | Yes      | Date and time of appointment                   |
| `duration`           | VARCHAR(10)  | Yes      | Duration (e.g. "30m")                          |
| `clinician`          | VARCHAR(255) | Yes      | Name of the clinician                          |
| `department`         | VARCHAR(50)  | Yes      | Department name             |
| `postcode`           | VARCHAR(10)  | Yes      | Location of appointment |


## Caveats
- I considered an ORM for database but in the timeframe could not decide on one
- Using Docker I planned to add a CRON based backup that would dump the database which could be time frame configurable 
- No localisation was done, if I was to implement it further I would use JSON translations such as `en.json, fr.json` etc  

## Getting running
### Requirements
- `docker >= 27` (so docker compose is enabled)
- `python3 >= 3.13.2`
- `pip >= 25`
### Running (Quick start)
``` bash
$ docker compose up --build
...
...
db-1   | 2025-07-21 13:53:59.764 UTC [1] LOG:  database system is ready to accept connections
api-1  | 
api-1  |    FastAPI   Starting production server 🚀

```

Assuming everything has worked in docker you should now be able to access on:
https://localhost:8000/api/{route}

**NOTE - YOU MAY NEED TO RUN `python3 populate_db.py` TO COPY THE EXAMPLE JSONS**

### API Documentation
For the documentation I decided to use Swagger UI built into FastAPI
After having everything running on docker, the Docs for the API should be accessible on:
https://localhost:8000/docs

This gives a pretty version or JSON accesible format of something like

``` json"paths": {
    "/api/patients": {
      "get": {
        "tags": [
          "patients"
        ],
        "summary": "Get all patients",
        "description": "Returns a list of all patients database.",
        "operationId": "get_patients_api_patients_get",
        "responses": {
          "200": {
            "description": "A list of patient objects.",
            "content": {
              "application/json": {
                "schema": {

                },
                "example": [
                  {
                    "nhs_number": "1234567890",
                    "name": "John Doe",
                    "date_of_birth": "1990-01-01",
                    "postcode": "SW1A 1AA"
                  }
                ]
              }
            }
          }
        }
      },
```

### Running (Advanced)
If you wish to avoid using docker (**NOT RECOMMENDED**) you can run locally using Python.

This was built using venv so will require some environment setup

``` bash
# Venv setup
$ python3 -m venv .
$ source bin/activate
... 
# Install
$ pip install --no-cache-dir -r requirements.txt
...
# Run
$ fastapi run src/main.py
```

**IMPORTANT**: The app will require the DB image being spun up indiviudally when this is done.




