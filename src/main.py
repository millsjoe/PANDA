import json
from fastapi import FastAPI
from routes.patients import router as patients_router
from routes.appointments import router as appointments_router

app = FastAPI()

app.include_router(patients_router)
app.include_router(appointments_router)


@app.get("/api/")
def read_root():
    return {"Hello": "World"}


        